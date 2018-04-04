class Post:
    def __init__(self,userId,topic,title,postContent,date):
        self.userId = userId
        self.topic = topic
        self.title = title
        self.postContent = postContent
        self.date = date
    def getUserId(self):
        return self.userId
    def getTopic(self):
        return self.topic
    def getTitle(self):
        return self.title
    def getPostContent(self):
        return self.postContent
    def getDate(self):
        return self.date
    def setUserId(self,userId):
        self.userId = userId
    def setTopic(self,topic):
        self.topic = topic
    def setTitle(self,title):
        self.title = title
    def setPostContents(self,content):
        self.postContent = content
    def setDate(self,date):
        self.date = date
    
    
