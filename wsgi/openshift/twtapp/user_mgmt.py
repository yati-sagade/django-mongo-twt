from documents import UserProfile, Post

def follow(follower=None, followee=None):
    '''Takes two UserProfile instances, and makes the follower follow the
    followee.'''
    if followee.username not in follower.followee:
        follower.followee.append(followee.username)
        follower.save()

    if follower.username not in followee.follower:
        followee.follower.append(follower.username)
        followee.save()
#-------------------------------------------------------------------------------
def unfollow(follower, followee):
    if followee.username in follower.followee:
        follower.followee.remove(followee.username)
        follower.save()

    if follower.username in followee.follower:
        followee.follower.remove(follower.username)
        followee.save()
#-------------------------------------------------------------------------------
