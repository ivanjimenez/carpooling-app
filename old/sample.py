import asyncio
import heapq

class Car:
    def __init__(self, car_id, seats):
        self.car_id = car_id
        self.seats = seats
        self.passengers = []

    def add_passenger(self, group_id, num_people):
        if len(self.passengers) + num_people <= self.seats:
            self.passengers.append((group_id, num_people))
            return True
        return False

class CarPoolService:
    def __init__(self, cars):
        self.available_cars = [Car(car['id'], car['seats']) for car in cars]
        self.waiting_groups = []

    async def request_ride(self, group):
        while True:
            for car in self.available_cars:
                if car.add_passenger(group['id'], group['people']):
                    print(f"Group {group['id']} assigned to car {car.car_id}")
                    if len(car.passengers) == car.seats:
                        self.available_cars.remove(car)
                    return
            await self.wait_for_car(group)

    async def wait_for_car(self, group):
        print(f"Group {group['id']} waiting for a car...")
        event = asyncio.Event()
        self.waiting_groups.append((group, event))
        await event.wait()

    async def assign_cars(self):
        while True:
            if self.waiting_groups:
                group, event = self.waiting_groups.pop(0)
                for car in self.available_cars:
                    if car.add_passenger(group['id'], group['people']):
                        print(f"Group {group['id']} assigned to car {car.car_id}")
                        if len(car.passengers) == car.seats:
                            self.available_cars.remove(car)
                        event.set()
                        break
                else:
                    new_car_id = max(c.car_id for c in self.available_cars) + 1
                    new_car = Car(new_car_id, group['people'])
                    new_car.add_passenger(group['id'], group['people'])
                    self.available_cars.append(new_car)
                    print(f"Group {group['id']} assigned to new car {new_car_id}")
                    event.set()
            await asyncio.sleep(0.1)  # Adjust sleep time as needed

# Define your data
cars = [
    {"id": 1, "seats": 4},
    {"id": 2, "seats": 6},
    {"id": 3, "seats": 5}
]
travelers = [
    {"id": 1, "people": 4},
    {"id": 2, "people": 3},
    # Add more travelers as needed
]

async def main():
    car_pool_service = CarPoolService(cars)
    tasks = [car_pool_service.request_ride(group) for group in travelers]
    tasks.append(car_pool_service.assign_cars())
    await asyncio.gather(*tasks)

asyncio.run(main())
