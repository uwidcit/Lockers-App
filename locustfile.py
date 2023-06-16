import time, uuid, random
from locust import User, HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task(5)
    def testLocker(self):
        self.client.get("/locker")
        payload = {
            "locker_code": str(uuid.uuid4()).split("-")[0]+"TEST4",
            "locker_type": "Small",
            "status": "Free",
            "key": "PASS",
            "area": "1"
        }

        response = self.client.post("/locker", data=payload)
        if response.status_code == 200:
            print("Form submitted successfully")
        else:
            print("Form submission failed")
        
    @task(1)
    def testArea(self):
        self.client.get("/area")
        payload = {
            "description": "ENGEN",
            "longitude": "10",
            "latitude": "12"
        }

        response = self.client.post("/area", data=payload)
        if response.status_code == 200:
            print("Form submitted successfully")
        else:
            print("Form submission failed")

    @task(4)
    def testTransactionLog(self):
        self.client.get("/transactionLog")

    @task(3)
    def testStudent(self):
        self.client.get("/student")
        payload = {
            "student_id": random.randint(10000000, 99999999),
            "f_name": "Kristopher",
            "l_name": "Bholai",
            "faculty": "FST",
            "p_no": "2927492",
            "email": str(uuid.uuid4()).split("-")[0]+"kristopher.bholai@gmail.com"
        }

        response = self.client.post("/student", data=payload)
        if response.status_code == 200:
            print("Form submitted successfully")
        else:
            print("Form submission failed")

    @task(2)
    def testRentType(self):
        self.client.get("/rentType")

    @task(4)
    def testKey(self):
        self.client.get("/key")
    
    @task(4)
    def testMasterkey(self):
        self.client.get("/masterkey")