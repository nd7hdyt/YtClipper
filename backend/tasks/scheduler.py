"""
ENtaskEN
configENexecuteENtask
"""

import logging
from celery import Celery
from celery.schedules import crontab

from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)


# configENtask
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """configENtask"""
    
    # EN2ENexecuteEN
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        cleanup_expired_data.s(days=30),
        name='daily_data_cleanup'
    )
    
    # ENexecuteENcheck
    sender.add_periodic_task(
        crontab(minute=0),
        check_data_consistency.s(),
        name='hourly_consistency_check'
    )
    
    # EN3ENexecuteEN
    sender.add_periodic_task(
        crontab(hour=3, minute=0, day_of_week=0),
        cleanup_orphaned_data.s(),
        name='weekly_orphaned_cleanup'
    )
    
    # EN1ENexecutesystemENcheck
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        health_check.s(),
        name='daily_health_check'
    )
    
    logger.info("ENtaskconfigEN")


def get_scheduled_tasks() -> dict:
    """fetchallENconfigENtask"""
    return {
        'daily_data_cleanup': {
            'schedule': 'EN2EN',
            'task': 'cleanup_expired_data',
            'description': 'EN（EN30EN）'
        },
        'hourly_consistency_check': {
            'schedule': 'EN',
            'task': 'check_data_consistency',
            'description': 'checkEN'
        },
        'weekly_orphaned_cleanup': {
            'schedule': 'EN3EN',
            'task': 'cleanup_orphaned_data',
            'description': 'EN'
        },
        'daily_health_check': {
            'schedule': 'EN1EN',
            'task': 'health_check',
            'description': 'systemENcheck'
        }
    }


def enable_scheduled_tasks():
    """ENtask"""
    try:
        # ENcanENtaskEN
        logger.info("ENtaskEN")
        return True
    except Exception as e:
        logger.error(f"ENtaskfailed: {e}")
        return False


def disable_scheduled_tasks():
    """ENtask"""
    try:
        # ENcanENtaskEN
        logger.info("ENtaskEN")
        return True
    except Exception as e:
        logger.error(f"ENtaskfailed: {e}")
        return False
