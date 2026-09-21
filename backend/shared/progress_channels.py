"""
ENprogressEN
EN
"""

def project_progress_channel(project_id: str) -> str:
    """
    generateprojectprogressEN
    
    Args:
        project_id: projectID
        
    Returns:
        EN: progress:project:<project_id>
    """
    # EN，EN"project_"
    return f"progress:project:{project_id}"

def task_progress_channel(task_id: str) -> str:
    """
    generatetaskprogressEN
    
    Args:
        task_id: taskID
        
    Returns:
        EN: progress:task:<task_id>
    """
    return f"progress:task:{task_id}"

def normalize_channel(raw: str) -> str:
    """
    EN，EN
    
    Args:
        raw: EN
        
    Returns:
        EN
    """
    if not raw:
        return ""
    
    s = raw.strip()
    
    # ifENprojectIDEN，ENprojectprogressEN
    if s.startswith("progress:project:"):
        return s
    elif s.startswith("project_"):
        # ENproject_EN，ENID
        project_id = s[8:]  # EN"project_"EN
        return project_progress_channel(project_id)
    elif s.startswith("progress:project_"):
        # processingprogress:project_<id>EN
        project_id = s[17:]  # EN"progress:project_"EN
        return project_progress_channel(project_id)
    else:
        # ENprojectID
        return project_progress_channel(s)
