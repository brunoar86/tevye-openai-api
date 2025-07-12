from fastapi import APIRouter

router = APIRouter()


@router.get('/live', tags=['Health'])
def live():
    '''
    Route to check liveness
    '''
    return {'message': 'Tevye OpenAI API is live!'}


@router.get('/ready', tags=['Health'])
def ready():
    '''
    Route to check readiness
    '''
    return {'message': 'Tevye OpenAI API is ready!'}