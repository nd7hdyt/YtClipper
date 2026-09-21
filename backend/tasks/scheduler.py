"""
translatedtasktranslated
configAndtranslated'stranslatedtask
"""

import logging
from celery import Celery
from celery.schedules import crontab

from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)


# configtranslatedtask
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """configtranslatedtask"""
    
    # pertranslated2translatedclean
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        cleanup_expired_data.s(days=30),
        name='daily_data_cleanup'
    )
    
    # pertranslatedonetranslatedcheck
    sender.add_periodic_task(
        crontab(minute=0),
        check_data_consistency.s(),
        name='hourly_consistency_check'
    )
    
    # pertranslated3translatedclean
    sender.add_periodic_task(
        crontab(hour=3, minute=0, day_of_week=0),
        cleanup_orphaned_data.s(),
        name='weekly_orphaned_cleanup'
    )
    
    # pertranslated1translatedSystemHealth Check
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        health_check.s(),
        name='daily_health_check'
    )
    
    logger.info("translatedtaskconfigtranslated")


def get_scheduled_tasks() -> dict:
    """fetchtranslatedconfig'stranslatedtask"""
    return {
        'daily_data_cleanup': {
            'schedule': 'pertranslated2translated',
            'task': 'cleanup_expired_data',
            'description': 'cleantranslated（translated30translated）'
        },
        'hourly_consistency_check': {
            'schedule': 'pertranslated',
            'task': 'check_data_consistency',
            'description': 'checktranslatedonetranslated'
        },
        'weekly_orphaned_cleanup': {
            'schedule': 'pertranslated3translated',
            'task': 'cleanup_orphaned_data',
            'description': 'cleantranslated'
        },
        'daily_health_check': {
            'schedule': 'pertranslated1translated',
            'task': 'health_check',
            'description': 'SystemHealth Check'
        }
    }


def enable_scheduled_tasks():
    """translatedusetranslatedtask"""
    try:
        # thistranslatedcantranslatedaddtranslatedusetranslatedtask'stranslated
        logger.info("translatedtasktranslateduse")
        return True
    except Exception as e:
        logger.error(f"translatedusetranslatedtaskfailed: {e}")
        return False


def disable_scheduled_tasks():
    """translatedusetranslatedtask"""
    try:
        # thistranslatedcantranslatedaddtranslatedusetranslatedtask'stranslated
        logger.info("translatedtasktranslateduse")
        return True
    except Exception as e:
        logger.error(f"translatedusetranslatedtaskfailed: {e}")
        return False
