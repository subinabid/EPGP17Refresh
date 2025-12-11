"""API views for the EPGP application."""

from django.contrib.auth.models import User  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.decorators import (  # type: ignore
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response  # type: ignore
from rest_framework.authentication import (  # type: ignore
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # type: ignore
from .serializers import (
    UserSerializer,
    DetailUserSerializer,
    BatchInfoSerializer,
    SocialLinksSerializer,
    ElectiveOfferingSmallSerializer,
    ElectiveEnrollmentSerializer,
    ElectiveDetailSerializer,
)
from .models import BatchInfo, SocialLinks, ElectiveOffering, ElectiveEnrollment


################################################################################
########## User Views
################################################################################


class ListUsers(APIView):
    """
    View to list all users in the system.
    * Only admin users are able to access this view.
    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_user(request):
    """
    Create a new user.

    Required fields: username, email, password
    Optional fields: first_name, last_name
    """
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        # Validate required fields
        if not all([username, email, password]):
            return Response(
                {"error": "username, email, and password are required"}, status=400
            )

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": f"User with username {username} already exists"}, status=400
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": f"User with email {email} already exists"}, status=400
            )

        # Create the user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            serializer = DetailUserSerializer(user)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change password for the authenticated user.

    Required fields: old_password, new_password
    """
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not all([old_password, new_password]):
        return Response(
            {"error": "old_password and new_password are required"}, status=400
        )

    user = request.user
    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect"}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password changed successfully"}, status=200)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def update_user_admin(request, pk):
    """Update an existing user by ID (admin only)

    Optional fields: email, first_name, last_name
    Use PUT for full update, PATCH for partial update.
    """
    return update_user(request, pk)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user_self(request):
    """Update the authenticated user's own information

    Optional fields: email, first_name, last_name
    Use PUT for full update, PATCH for partial update.
    """
    return update_user(request, request.user.id)


########################################
##  Helper function to update user


def update_user(request, pk):
    """
    Update an existing user by ID.

    Optional fields: email, first_name, last_name
    Use PUT for full update, PATCH for partial update.
    """
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": f"User with id {pk} does not exist"}, status=404)

    # Get update fields from request
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    # Check if email is being changed to an existing email
    if email and email != user.email:
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": f"User with email {email} already exists"}, status=400
            )
        user.email = email

    # Update other fields if provided
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    try:
        user.save()
        serializer = DetailUserSerializer(user)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


########################################


@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def userinfo(request):
    content = {
        "user": str(request.user),
        "auth": str(request.auth),
        "detail": DetailUserSerializer(request.user).data,
    }
    return Response(content)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_queryset(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = DetailUserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": f"User with id {pk} does not exist"}, status=404)


################################################################################
## User information
################################################################################


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def batch_info(request):
    """Get BatchInfo for a specific user by user ID."""
    if request.method == "GET":
        try:
            batch_info = BatchInfo.objects.get(user=request.user)
            serializer = BatchInfoSerializer(batch_info)
            return Response(serializer.data)
        except BatchInfo.DoesNotExist:
            return Response(
                {"error": f"No BatchInfo found for user {request.user}"}, status=404
            )

    elif request.method == "POST":
        try:
            batch_info_obj, created = BatchInfo.objects.get_or_create(user=request.user)
            serializer = BatchInfoSerializer(
                batch_info_obj, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                status_code = 201 if created else 200
                return Response(serializer.data, status=status_code)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response(
                {"error": f"User with id {request.user} does not exist"}, status=404
            )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def update_social_links(request):
    """Update SocialLinks for a specific user by user ID."""
    try:
        social_links = SocialLinks.objects.get(user=request.user)
    except SocialLinks.DoesNotExist:
        return Response(
            {"error": f"No SocialLinks found for user {request.user}"}, status=404
        )

    if request.method in ["PUT", "PATCH"]:
        serializer = SocialLinksSerializer(
            social_links, data=request.data, partial=(request.method == "PATCH")
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_social_links(request):
    """Get or create SocialLinks for a specific user by user ID."""
    if request.method == "GET":
        try:
            social_links = SocialLinks.objects.get(user__id=request.user.id)
            serializer = SocialLinksSerializer(social_links)
            return Response(serializer.data)
        except SocialLinks.DoesNotExist:
            return Response(
                {"error": f"No SocialLinks found for user {request.user}"}, status=404
            )

    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            social_links, created = SocialLinks.objects.get_or_create(user=user)
            serializer = SocialLinksSerializer(
                social_links, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                status_code = 201 if created else 200
                return Response(serializer.data, status=status_code)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response(
                {"error": f"User with id {request.user} does not exist"}, status=404
            )


################################################################################
## Electives
################################################################################


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_electives(request):
    """List all Elective offerings."""

    electives = ElectiveOffering.objects.all().order_by(
        "course__area", "course__course_code", "section"
    )
    serializer = ElectiveOfferingSmallSerializer(
        electives, many=True, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def elective_detail(request, pk):
    """Details of a specific Elective offering by ID."""

    try:
        elective_offering = ElectiveOffering.objects.get(id=pk)
        serializer = ElectiveDetailSerializer(
            elective_offering, context={"request": request}
        )
        return Response(serializer.data)
    except ElectiveOffering.DoesNotExist:
        return Response(
            {"error": f"ElectiveOffering with id {pk} does not exist"}, status=404
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def elective_takers(request, pk):
    """List of users enrolled in a specific Elective offering by ID."""

    try:
        elective_offering = ElectiveOffering.objects.get(id=pk)
        enrollments = ElectiveEnrollment.objects.filter(
            elective_offering=elective_offering
        )
        users = [enrollment.user for enrollment in enrollments]
        serializer = DetailUserSerializer(
            users, many=True, context={"request": request}
        )
        return Response(serializer.data)
    except ElectiveOffering.DoesNotExist:
        return Response(
            {"error": f"ElectiveOffering with id {pk} does not exist"}, status=404
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def enrolled_elective(request):
    """Enrolled electives of the authenticated user."""

    enrollments = ElectiveEnrollment.objects.filter(user=request.user)
    serializer = ElectiveEnrollmentSerializer(
        enrollments, many=True, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def enroll_elective(request, pk):
    """Enroll the authenticated user in an elective offering."""
    if request.method == "POST":
        try:
            elective_offering = ElectiveOffering.objects.get(id=pk)
        except ElectiveOffering.DoesNotExist:
            return Response(
                {"error": f"ElectiveOffering with id {pk} does not exist"}, status=404
            )

        # Check if already enrolled
        if ElectiveEnrollment.objects.filter(
            user=request.user, elective_offering=elective_offering
        ).exists():
            return Response(
                {"error": "User is already enrolled in this elective offering"},
                status=400,
            )

        # Enroll the user
        enrollment = ElectiveEnrollment.objects.create(
            user=request.user, elective_offering=elective_offering
        )
        serializer = ElectiveEnrollmentSerializer(enrollment)
        return Response(serializer.data, status=201)

    elif request.method == "GET":
        # Checck if the user is already enrolled and return True/False

        try:
            enrollments = ElectiveEnrollment.objects.filter(user=request.user)

            context = {
                "user": request.user.username,
                "elective_offering_id": pk,
                "elective": ElectiveOffering.objects.get(id=pk).course.__str__(),
                "enrolled": pk
                in [enrollment.elective_offering.id for enrollment in enrollments],
            }
            return Response(context)
        except ElectiveOffering.DoesNotExist:
            return Response(
                {"error": f"ElectiveOffering with id {pk} does not exist"}, status=404
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)
