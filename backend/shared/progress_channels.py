"""
translatedone'sprogresstranslated
translatedonetranslated'stranslatedissue
"""

def project_progress_channel(project_id: str) -> str:
    """
    translatedprojectprogresstranslated
    
    Args:
        project_id: projectID
        
    Returns:
        translatedone'stranslated: progress:project:<project_id>
    """
    # translatedoneusetranslated，translated"project_"
    return f"progress:project:{project_id}"

def task_progress_channel(task_id: str) -> str:
    """
    translatedtaskprogresstranslated
    
    Args:
        task_id: taskID
        
    Returns:
        translatedone'stranslated: progress:task:<task_id>
    """
    return f"progress:task:{task_id}"

def normalize_channel(raw: str) -> str:
    """
    translated，translatedoneformat
    
    Args:
        raw: translated
        
    Returns:
        translated'stranslated
    """
    if not raw:
        return ""
    
    s = raw.strip()
    
    # iftranslatedIsprojectIDformat，translatedprojectprogresstranslated
    if s.startswith("progress:project:"):
        return s
    elif s.startswith("project_"):
        # translatedproject_translated，translatedID
        project_id = s[8:]  # translated"project_"translated
        return project_progress_channel(project_id)
    elif s.startswith("progress:project_"):
        # processprogress:project_<id>format
        project_id = s[17:]  # translated"progress:project_"translated
        return project_progress_channel(project_id)
    else:
        # translatedIstranslatedprojectID
        return project_progress_channel(s)
