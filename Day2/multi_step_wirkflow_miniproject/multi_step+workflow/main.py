from chains import create_workflow


print("====================================")
print("     MULTI-STEP WORKFLOW APP")
print("====================================")


topic = input("\nEnter a topic: ")


print("\nProcessing your request...\n")


result = create_workflow(topic)


print("====================================")
print("              RESULT")
print("====================================")

print(result)