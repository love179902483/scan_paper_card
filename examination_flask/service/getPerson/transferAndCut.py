class TransferAndCut():
    '''
    转换得到的图片并且切割开
    获取到的标准外框信息进行处理和切割
    根据页数，get
    '''
    def __init__(self, imageGray, pageData):
        self.imageGray = imageGray
        self.pageData = pageData
        # studentID这个变量若本页没有则为None
        self.studentID = self.__getStudentID_Variable()
        # multipleChose这个变量若本页没有则为None
        self.multipleChose = self.__getMultipleChose_Variable()


    def getAllImages(self):
        if self.studentID is not None:
            self.__getStudentID()
        
        if self.multipleChose is not None:
            self.__getImageMultipleChose()

    def __getImageStudentID(self):
        print('获取学号')
    
    def __getImageMultipleChose(self):
        print('获取选择题答案')

    def __getStudentID_Variable(self):
        '''
            解析变量，获取学生ID信息
            若这一页有ID的信息则要处理
        '''
        returnValue = None
        for key in self.pageData.keys():
            if key == 'ID':
                returnValue = self.pageData['ID']
            else:
                continue

        return returnValue

    def __getMultipleChose_Variable(self):
        '''
            解析变量，获取选择题的框子信息
            若这一页有选择题的信息则要处理
        '''
        returnValue = None
        for key in self.pageData.keys():
            if key == 'MultipleChose':
                returnValue = self.pageData['MultipleChose']
            else:
                continue 

        return returnValue


    