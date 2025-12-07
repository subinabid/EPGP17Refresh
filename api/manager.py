"""Custom manager for the API app."""

from .models import Elective, Professor

electives_list = [
    "Advanced Corporate Communication: The Practitioner's Approach",
    "Agent-based Simulation for Business Analytics",
    "Artificial Intelligence for Business",
    "Blockchain for Business",
    "Cross Cultural Communication",
    "Cyber Security and Privacy",
    "Decoding Customer Engagement",
    "Game Theory",
    "Gen AI-Augmented Analytics",
    "Introduction to Public Policy",
    "Leading Self and Organization",
    "Leading with Linguistic and Social Intelligence",
    "Lean Six Sigma",
    "Managing Business Markets",
    "Marketing Meets Technology",
    "Mergers, Acquisitions and Strategic Alliances",
    "Product and Brand Management",
    "Project Finance",
    "Rural Society and India",
    "Security Analysis and Portfolio Management",
    "Strategic Marketing",
    "Strategy Implementation",
    "Supply Chain Analytics",
    "Supply Chain Management",
]


electives_details = [
    {
        "Course": "Advanced Corporate Communication: The Practitioner's Approach",
        "Code": "EHLAM-002",
        "Faculty": "Prof. Deepa Sethi",
    },
    {
        "Course": "Agent-based Simulation for Business Analytics",
        "Code": "EECO-002",
        "Faculty": "Prof. Vipin P Veetil",
    },
    {
        "Course": "Artificial Intelligence for Business",
        "Code": "EIS-001",
        "Faculty": "Prof. M P Sebastian",
    },
    {
        "Course": "Blockchain for Business",
        "Code": "EIS-002",
        "Faculty": "Prof. Kalpit Sharma",
    },
    {
        "Course": "Cross Cultural Communication",
        "Code": "EHLAM-004",
        "Faculty": "Prof. Deepa Sethi",
    },
    {
        "Course": "Cyber Security and Privacy",
        "Code": "EIS-004",
        "Faculty": "Prof. Sreejith A",
    },
    {
        "Course": "Decoding Customer Engagement",
        "Code": "EMM-021",
        "Faculty": "Prof. Shaphali Gupta",
    },
    {"Course": "Game Theory", "Code": "EECO-003", "Faculty": "Prof. Anirban Ghatak"},
    {
        "Course": "Gen AI-Augmented Analytics",
        "Code": "EIS-012",
        "Faculty": "Dr. Pramukh Nanjundaswamy Vasist",
    },
    {
        "Course": "Introduction to Public Policy",
        "Code": "EECO-004",
        "Faculty": "Prof. Sthanu R Nair",
    },
    {
        "Course": "Leading Self and Organization",
        "Code": "EOBHR-006",
        "Faculty": "Prof. Priya Nair Rajeev",
    },
    {
        "Course": "Leading with Linguistic and Social Intelligence",
        "Code": "EHLAM-008",
        "Faculty": "Prof. Anupam Das",
    },
    {"Course": "Lean Six Sigma", "Code": "EQMOM-003", "Faculty": "Prof. Saji Gopinath"},
    {
        "Course": "Managing Business Markets",
        "Code": "EMM-006",
        "Faculty": "Prof. Joffi Thomas",
    },
    {
        "Course": "Marketing Meets Technology",
        "Code": "EMM-010",
        "Faculty": "Prof. Priya Narayanan",
    },
    {
        "Course": "Mergers, Acquisitions and Strategic Alliances",
        "Code": "ESM-006",
        "Faculty": "Prof. Kamal Kishore Sharma",
    },
    {
        "Course": "Product and Brand Management",
        "Code": "EMM-014",
        "Faculty": "Prof. Joshy Joseph / Prof. Sreejesh S",
    },
    {
        "Course": "Project Finance",
        "Code": "EFAC-009",
        "Faculty": "Prof. Pankaj Kumar Baag",
    },
    {
        "Course": "Rural Society and India",
        "Code": "EHLAM-014",
        "Faculty": "Prof. Suraj Gogoi",
    },
    {
        "Course": "Security Analysis and Portfolio Management",
        "Code": "EFAC-011",
        "Faculty": "Mr. Venkatesh Bangaruswamy",
    },
    {
        "Course": "Security Analysis and Portfolio Management",
        "Code": "EFAC-011",
        "Faculty": "Prof. Sony Thomas",
    },
    {
        "Course": "Strategic Marketing",
        "Code": "EMM-019",
        "Faculty": "Prof. Pronobesh Banerjee",
    },
    {
        "Course": "Strategic Marketing",
        "Code": "EMM-019",
        "Faculty": "Prof. Pronobesh Banerjee",
    },
    {
        "Course": "Strategy Implementation",
        "Code": "ESM-009",
        "Faculty": "Prof. Anita Kerai",
    },
    {
        "Course": "Supply Chain Analytics",
        "Code": "EQMOM-010",
        "Faculty": "Prof. Ramesh Krishnan",
    },
    {
        "Course": "Supply Chain Management",
        "Code": "EQMOM-009",
        "Faculty": "Prof. Sidhartha S Padhi",
    },
]


def is_valid_elective(elective_name: str) -> bool:
    """Check if the given elective name is valid."""
    return elective_name in electives_list


def add_all_electives() -> dict:
    """
    Add all electives from electives_list to the Elective model.

    Returns:
        dict: Contains created and existing counts
    """
    created_count = 0
    existing_count = 0
    errors = []

    for elective_name in electives_list:
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
    for elective in electives_details:
        faculty_name = elective.get('Faculty', '').strip()
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
            errors.append({
                'faculty': faculty_name,
                'error': str(e)
            })
    
    return {
        'created': created_count,
        'existing': existing_count,
        'total_processed': created_count + existing_count,
        'errors': errors,
        'message': f'Successfully added {created_count} new faculty members. {existing_count} faculty already existed.'
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
    
    for elective_detail in electives_details:
        try:
            course_name = elective_detail.get('Course', '').strip()
            course_code = elective_detail.get('Code', '').strip()
            faculty_name = elective_detail.get('Faculty', '').strip()
            
            if not course_name or not course_code:
                errors.append({
                    'elective': elective_detail,
                    'error': 'Missing course name or code'
                })
                continue
            
            # Get or create professor
            professor = None
            if faculty_name:
                professor, _ = Professor.objects.get_or_create(name=faculty_name)
            
            # Get or create elective
            elective, created = Elective.objects.get_or_create(
                course_code=course_code,
                course_name=course_name,
                defaults={
                    'instructor': professor
                }
            )
            
            if created:
                created_count += 1
            else:
                existing_count += 1
                
        except Exception as e:
            errors.append({
                'elective': elective_detail.get('Course', 'Unknown'),
                'error': str(e)
            })
    
    return {
        'created': created_count,
        'existing': existing_count,
        'total_processed': created_count + existing_count,
        'errors': errors,
        'message': f'Successfully added {created_count} new electives with faculty. {existing_count} electives already existed.'
    }
