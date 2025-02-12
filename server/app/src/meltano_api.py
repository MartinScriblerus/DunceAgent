# import os
# from meltano.core.project import Project
# from meltano.core.elt_context import ELTContextBuilder
# # from meltano.core.elt import ELT

# # Set the MELTANO_PROJECT_ROOT environment variable to the path of your Meltano project
# os.environ["MELTANO_PROJECT_ROOT"] = "../../../meltano_project/"

# # Load the Meltano project
# project = Project.find()

# # Create an ELT context
# context = ELTContextBuilder(project).with_session().context()

# # Run an ELT pipeline using tap-github as extractor and target-postgres as loader
# # elt = ELT(project)
# # elt.run(context, 'tap-github', 'target-postgres')