from robot.api.deco import library 
from robot.libraries.BuiltIn import BuiltIn
import json
import sys
from requests import Session
from icdc.requestswithsystemca import setup_session
from requests.auth import HTTPBasicAuth
import os

# fill the proxy
proxies =  {}



class Gamera : 
    
   """
         Get all the gherkins and Bdd Test implemented in SQUASH from gamera api

   """

   def __init__(self, username, password) :
        
        self.username = username 
        self.password = password
        self.projectId = int()
        self.listTests = []
        self.listTestsFromFolders = []
        self.listCasesFromFolders = None
        self.gerkhinTestIds = []
        self.gherkinsScript = {}
        self.BddTests = [] 
        
                           
        

   def GetProjectId(self) : 
       """
            Retrieve the Id of a project in gamera
            Return an integer
       """

       self.session = Session()
       setup_session(self.session)
       self.response = self.session.get(self.gameraApi + "projects/", auth = HTTPBasicAuth(self.username,self.password))
       #print(self.response)
       self.response_json = self.response.json()
       #print(self.response_json)
       self.projectId = int(self.response_json["_embedded"]["projects"][0]["id"])
       
       return self.projectId
       

        


   def GetListTests(self) :
      """
            Retrieve all the types of test implemented in a project
            Return a json

      """
      self.projectId = self.GetProjectId()
      #print(self.projectId)
      self.session = Session()
      setup_session(self.session)
      self.response = self.session.get(self.gameraApi + "projects/" + str(self.projectId) + "/test-cases-library/content", auth = HTTPBasicAuth(self.username,self.password))
      #print(self.response)
      self.response_json = self.response.json()
      self.listTests = self.response_json

      return self.listTests 


   def GetTestCasesFromFolders(self) : 
       """
         Retrieve the tests present in a folder
         Return a json
       
       """
       self.session = Session()
       setup_session(self.session)
       self.response = self.session.get(self.gameraApi + "test-case-folders/" , auth = HTTPBasicAuth(self.username,self.password))
       self.listCasesFromFolders= self.response.json()

       return self.listCasesFromFolders
   

   def GetTestListFromFolders(self) : 
       """
            Retrieve all the tests from folders
            Return a list of json
       
       """
       self.listCasesFromFolders = self.GetTestCasesFromFolders() 
       for dic in self.listCasesFromFolders["_embedded"]["test-case-folders"] : 
           self.session = Session()
           setup_session(self.session)
           self.response = self.session.get(self.gameraApi + "test-case-folders/" + str(dic["id"]) + "/content", auth=HTTPBasicAuth(self.username,self.password))
           self.response_json = self.response.json() 
           self.listTestsFromFolders.append(self.response_json)

       return self.listTestsFromFolders



   def GetGerkhinTestId(self) : 
       """
            Retrieve all gerkhins ID
            Return a list of tupe (name,id)

       """
       i = 0
       self.listTests = self.GetListTests()
       self.listTestsFromFolders = self.GetTestListFromFolders()
       #print(self.listTestsFromFolders)
       for dic in self.listTests["_embedded"]["test-case-library-content"] : 
           if dic["_type"] == "scripted-test-case" : 
               self.gerkhinTestIds.append((dic["name"],dic["id"]))
       while i < len(self.listTestsFromFolders) :
         if "_embedded" in self.listTestsFromFolders[i] :
            for dic_content in self.listTestsFromFolders[i]["_embedded"]["content"] :
               if dic_content["_type"] == "scripted-test-case" :
                  self.gerkhinTestIds.append((dic_content["name"],dic_content["id"]))
         i+=1
      
       return self.gerkhinTestIds


   def GetGerkhinsScripts(self) : 
       """
            Retrieve all tests scripts of type gerkhins
            Return a map 

       """
       self.gerkhinTestIds = self.GetGerkhinTestId()
       self.session = Session()
       setup_session (self.session)
       for gerkhinTestId in self.gerkhinTestIds : 
           self.response = self.session.get(self.gameraApi + "/test-cases/" + str(gerkhinTestId[1]), auth = HTTPBasicAuth(self.username,self.password))
           #print(self.response)
           self.response_json = self.response.json()
           #print(self.response_json)
           #print(self.response_json["script"])
           self.gherkinsScript[gerkhinTestId[0]] = [str(self.response_json["script"])]
       return self.gherkinsScript
       




class RobotFramework(Gamera) : 
    
    """
         Implement the script got from gamera in RBF 

    """

    pass








if __name__=="__main__" :
    
    project = Gamera("","")
    #project.GetProjectId()
    #print(project.projectId)
    #print(project.GetListTests())
    print(project.GetGerkhinsScripts())
