import time
from locust import User, HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task(5)
    def testLocker(self):
        self.client.get("/locker")
    
    @task(1)
    def testArea(self):
        self.client.get("/area")

    @task(4)
    def testTransactionLog(self):
        self.client.get("/transactionLog")

    @task(3)
    def testStudent(self):
        self.client.get("/student")

    @task(2)
    def testRentType(self):
        self.client.get("/rentType")

    @task(4)
    def testKey(self):
        self.client.get("/key")
    
    @task(4)
    def testMasterkey(self):
        self.client.get("/masterkey")