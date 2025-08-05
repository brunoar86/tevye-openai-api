from fastapi import APIRouter

from tevye_openai_api.app.utils.logger import log

router = APIRouter()


@router.get('/live', tags=['Health'])
def live():
    '''
    Route to check liveness
    '''
    log.info("Liveness check called")
    return {'message': 'Tevye OpenAI API is live!'}


@router.get('/ready', tags=['Health'])
def ready():
    '''
    Route to check readiness
    '''
    log.info("Readiness check called")
    return {'message': 'Tevye OpenAI API is ready!'}
