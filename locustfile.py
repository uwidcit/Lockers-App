import time
from locust import User, HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task(5)
    def testLocker(self):
        self.client.get("/locker")
        payload = {
            "locker_code": "TEST",
            "locker_type": "Small",
            "status": "Free",
            "key": "PASS",
            "area": "1"
        }

        headers = {"Content-Type": "form-data;"}
        response = self.client.post("/locker", data=payload, headers = headers)
        if response.status_code == 200:
            print("Form submitted successfully")
        else:
            print("Form submission failed")
        
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