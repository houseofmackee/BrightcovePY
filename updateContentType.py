"""
Example script to update content type for videos in an account
"""
from mackee import main, get_oauth
from brightcove.utils import static_vars
from brightcove.Audience import Audience

# get Audience API instance
@static_vars(aapi=None)
def get_audience() -> Audience:
    """
    Returns an Audience API instance. Creates one if it doesn't exist yet.
    """
    if not get_audience.aapi:
        get_audience.aapi = Audience(get_oauth())
    return get_audience.aapi

#===========================================
# callback to set content type for videos
#===========================================
def update_content_type(video: dict):
    """
    Updates content type for a video.
    """
    # get video ID and specify content type
    video_id = video.get('id')
    content_type = 'my-type-here'

    # make API call
    response = get_audience().SetContentType(video_id=video_id, content_type=content_type)

    # check if we have a success response
    if response.status_code in [200,202]:
        print(f'Updated content type for video ID {video_id} with status {response.status_code}.')
    else:
        print(f'Error code {response.status_code} updating content type for video ID {video_id}:')
        print(response.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(update_content_type)
