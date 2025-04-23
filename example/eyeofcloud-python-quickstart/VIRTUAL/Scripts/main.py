import random
from eyeofcloud import eyeofcloud

eyeofcloud_client = eyeofcloud.Eyeofcloud(sdk_key="1000122_2e2d7fbdea1afc51")

if not eyeofcloud_client.config_manager.get_config():
    raise Exception("Eyeofcloud client invalid. Verify in Settings>Environments that "
                    "you used the primary environment's SDK key")


on_flags = False

for _ in range(10):
    # --------------------------------
    # to get rapid demo results, generate random users.
    # Each user always sees the same variation unless you reconfigure the flag rule.
    # --------------------------------
    user_id = str(random.randrange(1000, 9999))
    # --------------------------------
    # Create hardcoded user & bucket user into a flag variation
    # --------------------------------
    user = eyeofcloud_client.create_user_context(user_id)
    # "product_sort" corresponds to a flag key in your Eyeofcloud project
    decision = user.decide("buy")

    if not decision.variation_key:
        print(f"decision error {', '.join(decision.reasons)}")

    sort_method = decision.variables["json_variable"]

    # --------------------------------
    # Mock what the users sees with print statements
    # (in production, use flag variables to implement feature configuration)
    # --------------------------------

    # always returns false until you enable a flag rule in your Eyeofcloud project
    if decision.enabled:
        on_flags = True
    print(
        f"\nFlag {'on' if decision.enabled else 'off'}. User number {user.user_id} saw flag variation: {decision.variation_key}"
        f" and got products sorted by: {sort_method} config variable as part of flag rule: {decision.rule_key}"
    )

project_id = eyeofcloud_client.config_manager.get_config().project_id

if not on_flags:
    print("Flag was off for everyone. Some reasons could include:")
    print("1. Your sample size of visitors was too small. Rerun, or increase the iterations in the FOR loop")
    print("2. By default you have 2 keys for 2 project environments (dev/prod). Verify in Settings>Environments "
            "that you used the right key for the environment where your flag is toggled to ON.")
    print(f"Check your key at https://app.eyeofcloud.com/v2/projects/{project_id}/settings/implementation")