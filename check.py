import fileinput
import git
from git import repo


def change_version_for_pa_engine_properties(filepath, field_to_replace_split, value):
    version = 0
    with fileinput.FileInput(filepath, inplace=True) as file:
        for line in file:
            if field_to_replace_split in line:
                version = line.split(field_to_replace_split)[1]
                print(line.replace(version, value), end='\n')
            else:
                print(line, end="")
    print(field_to_replace_split + version + "has been changed to: " + value)


def change_JARversion_for_pyfiles(filepath, field_to_replace_split, value):
    version = 0
    with fileinput.FileInput(filepath, inplace=True) as file:
        for line in file:
            if field_to_replace_split in line:
                version = line.split(field_to_replace_split)[1]

                print(line.replace(version, value + ".jar\""), end='\n')
            else:
                print(line, end="")
    print(field_to_replace_split + version + " has been changed to: " + value)


if __name__ == '__main__':
    print("---------------------")
    print("ENGINE RELEASE SCRIPT")
    print("---------------------")
    print("PLEASE CREATE A PATCH OF YOUR LOCAL CHANGES AND REVERT BEFORE CONTINUING")

    engineVersion = input("Enter current engineVersion (required): ")

    if not (engineVersion):
        exit("engine version is required")

    stageVersion = input("Enter current stageVersion (optional): ")

    print("Changed Version:")
    print("-------------------------------------")
    print("engineVersion= ", engineVersion)
    if stageVersion:
        print("stageVersion= ", stageVersion)
    print("-------------------------------------")
    reply = input("Are versions are correct to commit (y/n)? ")

    if reply == "n" or reply == "N":
        exit("Enter versions again!")

    # pull is working
    # repository= git.Repo('pa-engine')
    # repository.git.checkout('develop')
    # origin = repository.remote(name='origin')
    # origin.pull()

    repository = git.Repo('/home/Abhishek.Thapa/Desktop/SimpleWebsite-with-Django_user_model')
    repository.git.checkout('usermodelframeworkbranch')
    origin = repository.remote(name='origin')
    origin.pull()

    # change the file input to ../src/main/resources/pa_engine_version.properties
    change_version_for_pa_engine_properties("checktest", "engineVersion=", engineVersion)
    # change the file input to ../src/main/resources/pa_engine_version.properties
    if stageVersion:
        change_version_for_pa_engine_properties("checktest", "stageVersion=",
                                                stageVersion)

    # update engine version in pom.xml

    # change file location to "../pom.xml"
    with fileinput.FileInput("checktest", inplace=True) as file:
        version = 0
        for line in file:
            if "<version>" in line:
                version = line.split("<version>")[1]
                print(line.replace(version, engineVersion + "</version>"), end='\n')
            else:
                print(line, end="")

        print("version changed to: ", engineVersion, " in pom.xml")

    # change jarversion for bash and python scripts.
    change_JARversion_for_pyfiles("checktest", "DasCascading-", engineVersion)

    # # update processing scripts
    # change_JARversion_for_pyfiles("../src/main/resources/dasProduction/jobs/production_cascading.py", "DasCascading-", engineVersion)
    # change_JARversion_for_pyfiles("../src/main/resources/dasProduction/jobs/emr_production_cascading.py", "DasCascading-", engineVersion)
    #
    # # # update parallel processing script
    # change_JARversion_for_pyfiles("../src/main/resources/dasProduction/jobs/parallel_emr_production_cascading.py", "DasCascading-", engineVersion)
    #
    # # # update real time migration script
    # change_JARversion_for_pyfiles("../src/main/resources/dasProduction/jobs/realTime_migration.py", "DasCascading-", engineVersion)
    #
    # # # update masterTables.sh
    # change_JARversion_for_pyfiles("../src/main/resources/dasProduction/bin/masterTables.sh", "DasCascading-", engineVersion)
    #
    # # # update historicalToPx.sh
    # change_JARversion_for_pyfiles("historicalToPx.sh", "DasCascading-", engineVersion)
    #
    # # # update historicalToPxEmr.sh
    # change_JARversion_for_pyfiles("../src/main/resources/dasProduction/bin/historicalToPxEmr.sh", "DasCascading-", engineVersion)

    repository.git.add("./check.py","./checktest")
    repository.git.commit('-m', 'Changed engine and master table versions and processing scripts for Engine Release V ' + engineVersion)
    origin = repository.remote(name='origin')
    origin.push()