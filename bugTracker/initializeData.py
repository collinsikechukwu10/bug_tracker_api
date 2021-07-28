import random
from bugTracker.models.service import Project, Task


def initialize():
    initialize_bug_tracker_models()


def initialize_bug_tracker_models():
    if Project.objects.count() == 0:
        print("No projects found, creating test samples...")
        for i in range(3):
            name = f"Project_{i}"
            proj = Project(name=name)
            proj.save()
            print(f"- Created Project `{name}`, populating sample tasks for it")
            for j in range(random.randint(3, 19)):
                tsk = Task(project=proj, reporter=None, title=f"Task{i}_{j}",
                           description=f"description for task {j} for project {i}")
                tsk.save()
