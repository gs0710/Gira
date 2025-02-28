from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["college"]  # Replace with your database name
collection = db["students"]  # Replace with your collection name

def send_message_to_parent(student_id):
    # Find the student record using student ID
    student = collection.find_one({"student_id": student_id})

    if student:
        parent_name = student.get("parent_name")
        parent_contact = student.get("parent_contact")

        if parent_name and parent_contact:
            message = f"Dear {parent_name}, your child {student['name']} is currently in the college."
            
            # Here you can implement the logic to send the message, e.g., SMS, email, etc.
            # For demonstration, we'll just print the message
            print(f"Message sent to {parent_contact}: {message}")
        else:
            print("Parent contact details are missing.")
    else:
        print("Student not found.")

# Example Usage
if __name__ == "__main__":
    student_id = input("Enter student ID: ")
    send_message_to_parent(student_id)
