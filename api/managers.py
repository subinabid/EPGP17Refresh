"""Custom manager for the API app."""

import csv
import json
from .models import Elective, Professor, StudyCenter, StudyCentrePOC
from .data import electives_list_q5, electives_details_q5


def is_valid_elective(elective_name: str) -> bool:
    """Check if the given elective name is valid."""
    return elective_name in electives_list_q5


def add_all_electives() -> dict:
    """
    Add all electives from electives_list to the Elective model.

    Returns:
        dict: Contains created and existing counts
    """
    created_count = 0
    existing_count = 0
    errors = []

    for elective_name in electives_list_q5:
        try:
            # Check if elective already exists
            elective, created = Elective.objects.get_or_create(
                course_name=elective_name,
                defaults={
                    "course_code": elective_name[:20],  # Use first 20 chars as code
                },
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        except Exception as e:
            errors.append({"elective": elective_name, "error": str(e)})

    return {
        "created": created_count,
        "existing": existing_count,
        "total_processed": created_count + existing_count,
        "errors": errors,
        "message": f"Successfully added {created_count} new electives. {existing_count} electives already existed.",
    }


def add_all_faculty() -> dict:
    """
    Add all faculty members from electives_details to the Professor model.

    Returns:
        dict: Contains created and existing counts with statistics
    """
    created_count = 0
    existing_count = 0
    errors = []
    faculty_set = set()

    # Extract unique faculty from electives_details
    for elective in electives_details_q5:
        faculty_name = elective.get("Faculty", "").strip()
        if faculty_name:
            faculty_set.add(faculty_name)

    for faculty_name in faculty_set:
        try:
            # Check if faculty already exists
            professor, created = Professor.objects.get_or_create(
                name=faculty_name,
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        except Exception as e:
            errors.append({"faculty": faculty_name, "error": str(e)})

    return {
        "created": created_count,
        "existing": existing_count,
        "total_processed": created_count + existing_count,
        "errors": errors,
        "message": f"Successfully added {created_count} new faculty members. {existing_count} faculty already existed.",
    }


def add_electives_with_faculty() -> dict:
    """
    Add all electives with their course codes and faculty from electives_details.

    Returns:
        dict: Contains created and existing counts with statistics
    """
    created_count = 0
    existing_count = 0
    errors = []

    for elective_detail in electives_details_q5:
        try:
            course_name = elective_detail.get("Course", "").strip()
            course_code = elective_detail.get("Code", "").strip()
            faculty_name = elective_detail.get("Faculty", "").strip()

            if not course_name or not course_code:
                errors.append(
                    {
                        "elective": elective_detail,
                        "error": "Missing course name or code",
                    }
                )
                continue

            # Get or create professor
            professor = None
            if faculty_name:
                professor, _ = Professor.objects.get_or_create(name=faculty_name)

            # Get or create elective
            elective, created = Elective.objects.get_or_create(
                course_code=course_code,
                course_name=course_name,
                defaults={"instructor": professor},
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        except Exception as e:
            errors.append(
                {"elective": elective_detail.get("Course", "Unknown"), "error": str(e)}
            )

    return {
        "created": created_count,
        "existing": existing_count,
        "total_processed": created_count + existing_count,
        "errors": errors,
        "message": f"Successfully added {created_count} new electives with faculty. {existing_count} electives already existed.",
    }


################################################################################
# Student List for EPGP 2017 Batch
################################################################################


# def add_students() -> dict:
#     """
#     Add all students from STUDENT_A_BATCH_2017 to the User model.

#     Returns:
#         dict: Contains created and existing counts with statistics
#     """
#     created_count = 0
#     existing_count = 0
#     errors = []

#     for student in STUDENT_A_BATCH_2017:
#         try:
#             full_name: str = student["name"]
#             first_name, *last_name_parts = full_name.split()
#             last_name = " ".join(last_name_parts) if last_name_parts else ""
#             username = f"{first_name}{student['rollNumber']}a".lower()

#             # Check if user already exists
#             user, created = User.objects.get_or_create(
#                 username=username,
#                 defaults={
#                     "first_name": first_name,
#                     "last_name": last_name,
#                     "password": username,
#                 },
#             )

#             if created:
#                 created_count += 1
#             else:
#                 existing_count += 1

#         except Exception as e:
#             errors.append({"student": student.get("name", "Unknown"), "error": str(e)})

#     return {
#         "created": created_count,
#         "existing": existing_count,
#         "total_processed": created_count + existing_count,
#         "errors": errors,
#         "message": f"Successfully added {created_count} new students. {existing_count} students already existed.",
#     }


# def fix_pwd() -> dict:
#     """
#     Fix missing passwords for all students in STUDENT_A_BATCH_2017.

#     Note: Don't run this function unless absolutely necessary.
#     """
#     updated_count = 0
#     errors = []

#     users = User.objects.all()

#     for user in users:
#         try:
#             if not user.username == "sabid":  # Skip sabid
#                 user.set_password(user.username)
#                 user.save()
#                 updated_count += 1

#         except Exception as e:
#             errors.append({"user": user.username, "error": str(e)})

#     return {
#         "updated": updated_count,
#         "errors": errors,
#         "message": f"Successfully updated passwords for {updated_count} users.",
#     }


# def fix_usernames() -> dict:
#     """
#     Fix usernames for all students in STUDENT_A_BATCH_2017.

#     Note: Don't run this function unless absolutely necessary.
#     """
#     updated_count = 0
#     errors = []
#     usernamefix = dict()

#     for student in STUDENT_A_BATCH_2017:
#         full_name = student["name"]
#         first_name, *last_name_parts = full_name.split()
#         wrong_username = f"{first_name}{student['rollNumber']}a".lower()
#         right_username = f"{first_name}17a".lower()
#         usernamefix[wrong_username] = right_username

#     print(usernamefix)

#     users = User.objects.all()

#     for user in users:
#         try:
#             #
#             if user.username in usernamefix:
#                 user.username = usernamefix[user.username]
#                 user.password = usernamefix[user.username]  # Set password to username
#                 user.save()
#                 updated_count += 1
#             else:
#                 print(f"Username {user.username} not in fix list.")
#         except Exception as e:
#             errors.append({"user": user.username, "error": str(e)})

#     return {
#         "updated": updated_count,
#         "errors": errors,
#         "message": f"Successfully updated usernames for {updated_count} users.",
#     }


################################################################################
# Study Centres
################################################################################


def loadStudyCentres():
    datafile = "locs_processed.csv"
    with open(datafile, "r", newline="") as sc:
        info = csv.DictReader(sc)
        print("Processing.....")
        for row in info:
            centre = StudyCenter.objects.create(
                state=row.get("State", "NA"),
                city=row.get("City", "NA"),
                location=row.get("Location", "NA"),
                address=row.get("Address", "NA"),
                pin=row.get("Pincode", "NA"),
            )
            print("Study centre added", centre)

            contacts = json.loads(row.get("poc_json", []))
            if len(contacts) > 0:
                for contact in contacts:
                    poc = StudyCentrePOC.objects.create(
                        centre=centre, person=contact["name"], number=contact["number"]
                    )
                    print("POC added", poc)
        print("End of CSV")
    print("Complete")
