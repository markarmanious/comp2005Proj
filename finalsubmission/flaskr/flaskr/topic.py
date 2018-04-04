
class Topic:
    def __init__(self,title,userId,subscribers={},posts=[]):
        self.userId = userId
        self.title = title
        self.subs = subscribers
        self.posts = posts
    def getUserId(self):
        return self.userId
    def getTitle(self):
        return self.title
    def getSubs(self):
        return self.subs
    def getPosts(self):
        return self.posts
    def setUserId(self,userId):
        self.userId= userId
    def setTopic(self,topic):
        self.topic = topic
    def setSubs(self,subs):
        self.subs = subs
    def setPosts(self,posts):
        self.posts = posts
    def addSub(self,userId):
        self.subs[userId]= false
    def userExists(self,userId):
        if(self.subs_has_key(userId)):
           return True
        else:
            print "the user " + e.userId + " is not in the subscribers list"
	    return False

    def notifySub(self,userId):
        if (self.userExists(userId)):
            self.subs[userId] = true
           
    def userIsNotified(self,userId):
        if (self.userExists(userId)):
           return self.subs[userId]
    
           
           

        

           
