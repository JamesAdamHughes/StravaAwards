class Node:

    def __init__(self, level, sDate, eDate):
        self.level          = level # week, month, year, day
        self.startDate      = sDate # Starting range of nide
        self.eDate          = eDate # End date of node
        self.children       = [] #child Nodes (days of week, week of months)
        self.isActivityNode = False

    # Given a 
    def isDateInNode(self, date):
        if date > self.eDate:
            return 1
        elif date < self.sDate:
            return -1
        else:
            return 0

    def containsLeaftNodes(self):
        return len(self.children)



    def getSubNode(self, target):
        # find which subnode contains the dates of target
        for child in self.children:
            if(child.isDateInNode(targetDate)):
                pass
