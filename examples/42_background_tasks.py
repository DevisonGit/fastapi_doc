from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


# background tasks
def write_notification(email: str, message=''):
    with open('log.txt', mode='w') as email_file:
        content = f'notification for {email}: {message}'
        email_file.write(content)


@app.post('/send-notification/{email}')
async def send_notification(email: str, backgound_tasks: BackgroundTasks):
    backgound_tasks.add_task(
        write_notification, email, message='some notification'
    )
    return {'message': 'notification sent in the background'}


# dependency injection
def write_log(message: str):
    with open('log.txt', mode='a') as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f'found query: {q}\n'
        background_tasks.add_task(write_log, message)
    return q


@app.post('/send-notification/{email}')
async def senf_notification(
    email: str, 
    background_taks: BackgroundTasks, 
    q: Annotated[str, Depends(get_query)]
):
    message = f'message to {email}\n'
    background_taks.add_task(write_log, message)
    return {'message': 'message sent'}