"""API views for the EPGP application."""

from django.contrib.auth.models import User  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.decorators import (  # type: ignore
    api_view,
    permission_classes,
)
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # type: ignore
from .serializers import (
    SCSerilazer,
    POCSerializer,
    UserSerializer,
    UserBatchSerializer,
    DetailUserSerializer,
    BatchInfoSerializer,
    SocialLinksSerializer,
    ElectiveSerializer,
    ElectiveOfferingSmallSerializer,
    ElectiveEnrollmentSerializer,
    ElectiveDetailSerializer,
)
from .models import (
    StudyCenter,
    StudyCentrePOC,
    BatchInfo,
    SocialLinks,
    Elective,
    ElectiveOffering,
    ElectiveEnrollment,
)


################################################################################
########## User Views
################################################################################


## /api/users/
class ListUsers(APIView):
    """
    View to list all users in the system.
    Only admin users are able to access this view.
    """

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)


## /api/users/create/
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


## /api/user/change-pwd/
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


## /api/users/update/id
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def update_user_admin(request, pk):
    """Update an existing user by ID (admin only)

    Optional fields: email, first_name, last_name
    Use PUT for full update, PATCH for partial update.
    """
    return update_user(request, pk)


## /api/users/update/
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user_self(request):
    """Update the authenticated user's own information

    Optional fields: email, first_name, last_name
    Use PUT for full update, PATCH for partial update.
    """
    return update_user(request, request.user.id)


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


## /api/user/
## /api/users/id/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def userinfo(request, pk=None):
    """Get detailed info of a user"""
    id = pk if pk else request.user.id
    try:
        user = User.objects.get(id=id)
        serializer = DetailUserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": f"User with id {id} does not exist"}, status=404)


################################################################################
## User information - Batch info, Social links and jobs (TBD)
################################################################################


def get_batch_info(user):
    """Helper function to get batch info by user"""
    try:
        batch_info = BatchInfo.objects.get(user=user)
        serializer = BatchInfoSerializer(batch_info)
        return Response(serializer.data)
    except BatchInfo.DoesNotExist:
        return Response({"error": f"No BatchInfo found for user {user}"}, status=404)


def update_batch_info(user, data):
    """Helper function to update batch info by user"""
    try:
        batch_info_obj, created = BatchInfo.objects.get_or_create(user=user)
        serializer = BatchInfoSerializer(batch_info_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_code = 201 if created else 200
            return Response(serializer.data, status=status_code)
        return Response(serializer.errors, status=400)
    except User.DoesNotExist:
        return Response({"error": f"User with id {user} does not exist"}, status=404)


def get_social_links(user):
    """Helper function to get social links by user"""
    try:
        social_links = SocialLinks.objects.get(user=user)
        serializer = SocialLinksSerializer(social_links)
        return Response(serializer.data)
    except SocialLinks.DoesNotExist:
        return Response({"error": f"No SocialLinks found for user {user}"}, status=404)


def update_social_link(user, data):
    """Helper function to update social ink by user"""
    try:
        social_links, created = SocialLinks.objects.get_or_create(user=user)
        serializer = SocialLinksSerializer(social_links, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_code = 201 if created else 200
            return Response(serializer.data, status=status_code)
        return Response(serializer.errors, status=400)
    except User.DoesNotExist:
        return Response({"error": f"User with id {user} does not exist"}, status=404)


## /api/user/batch
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def batch_info(request):
    """Get or update Batch Info for a logged in user"""
    if request.method == "GET":
        return get_batch_info(request.user)

    elif request.method == "POST":
        return update_batch_info(user=request.user, data=request.data)


## /api/users/id/batch
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def batch_info_by_id(request, pk):
    """Get Batch Info for a specific user by ID."""
    return get_batch_info(user=pk)


## /api/user/social
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def social_links(request):
    """Get or create SocialLinks for a logged in user."""
    if request.method == "GET":
        return get_social_links(request.user)

    elif request.method == "POST":
        return update_social_link(user=request.user, data=request.data)


## /api/users/id/social
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def social_links_by_id(request, pk):
    """Get SocialLinks for a specific user by user ID."""
    return get_social_links(user=pk)


################################################################################
## Electives
################################################################################


## /api/electives/all/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_all_electives(request):
    """List all elective subjects offered across years"""

    electives = Elective.objects.all().order_by("area", "course_code")
    serializer = ElectiveSerializer(
        electives,
        many=True,
        context={"request": request},
    )
    return Response(serializer.data)


## /api/electives/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_electives_for_user(request):
    """List all elective offerings for the user's batch."""

    batch = BatchInfo.objects.get(user=request.user).epgp_batch

    electives = ElectiveOffering.objects.filter(epgp_batch=batch).order_by(
        "course__area", "course__course_code", "section"
    )
    serializer = ElectiveOfferingSmallSerializer(
        electives,
        many=True,
        context={"request": request},
    )
    return Response(serializer.data)


## /api/electives/id/
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


## /api/electives/id/takers/
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
        serializer = UserBatchSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)
    except ElectiveOffering.DoesNotExist:
        return Response(
            {"error": f"ElectiveOffering with id {pk} does not exist"}, status=404
        )


# Helper function for a user's elective
def get_electives_by_user(user):
    """List all electives enrolled by a user"""
    enrollments = ElectiveEnrollment.objects.filter(user=user)
    serializer = ElectiveEnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data, status=200)


## /api/electives/enrolled/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def enrolled_elective(request):
    """Enrolled electives of the authenticated user."""
    return get_electives_by_user(user=request.user)


## /api/users/<int:pk>/electives/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def electives_by_user(request, pk):
    """Enrolled electives by a user"""
    return get_electives_by_user(user=pk)


## /api/electives/enroll/id/
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def enroll_elective(request, pk):
    """Get status of or enroll in an elective for logged in user
    POST: Enroll the authenticated user in an elective offering.
    GET: Return true if already enrolled else false"""
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


################################################################################
## Study Centre
################################################################################


## /api/centres/
class StudyCentresView(APIView):
    """List all study centres"""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        sc = StudyCenter.objects.all().order_by("state")
        serializer = SCSerilazer(sc, many=True, context={"request": request})
        return Response(serializer.data)


## /api/centres/id/POC
class StudyCentrePOCView(APIView):
    """List all study centre POCs"""

    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        poc = StudyCentrePOC.objects.filter(centre__id=id)
        serializer = POCSerializer(poc, many=True, context={"request": request})
        return Response(serializer.data)
