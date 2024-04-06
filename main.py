### IMPORTS
import os, asyncio, aiohttp
from pyfiglet import Figlet
from datetime import datetime
from rgbprint import gradient_print, Color

### VARIABLES
os.system("cls")
os.system("title mehhovcki - group checker v1")

with open("cookie.txt", "a") as file: file.close()

if open("cookie.txt", "r").read() != "":
    current_cookie = open("cookie.txt", "r").read()
else:
    current_cookie = ""
width = os.get_terminal_size().columns or 80

#### FUNCTIONS
def middle_text(text: str, width: int) -> str:
    padding: int = (width - len(text)) // 2
    return " " * padding + text

f = Figlet(font="elite", width=width)
t = f.renderText("mehhovcki group checker")
c = "\n".join(middle_text(t, width) for t in t.split("\n"))
print(middle_text(f"{Color(175, 149, 201)}version #1.1.1", width))

def handle_with_scans(mode: str):
    total_pending = total_funds = 0
    os.system(f"title {mode} scan - mehhovcki - group checker v1")
    print(middle_text(f"{Color(139, 59, 217)}Getting account data... {Color(255, 255, 255)}Please, wait a little..", 50))
    account_data: dict = asyncio.run(get_account_data())

    if account_data == {}:
        print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Account data was not found. Try new cookie next time. Press Enter to continue.", 50))
    else:
        showing_0_robux = show_ratelimit = False
        print(middle_text(f"{Color(139, 59, 217)}Account data was found! {Color(255, 255, 255)}Starting full scan on {account_data['name']} ({account_data['displayName']}).", 50))
        print(middle_text(f"Do you want to show groups, with 0 Robux on Funds, or Pending. Enter {Color(139, 59, 217)}\"y\"{Color(255, 255, 255)} to agree, or {Color(139, 59, 217)}\"n\"{Color(255, 255, 255)} to decline.", 50))
        new_choice = input(middle_text(f"{Color(139, 59, 217)}> {Color(255, 255, 255)}", 50))

        if new_choice.lower() == "y":
            showing_0_robux = True
        
        print(middle_text(f"Do you also want to get informed about ratelimits while checking?. Enter {Color(139, 59, 217)}\"y\"{Color(255, 255, 255)} to agree, or {Color(139, 59, 217)}\"n\"{Color(255, 255, 255)} to decline.", 50))
        new_choice = input(middle_text(f"{Color(139, 59, 217)}> {Color(255, 255, 255)}", 50))

        if new_choice.lower() == "y":
            show_ratelimit = True

        os.system("title pending scan - mehhovcki - group checker v1")
        groups: list = asyncio.run(get_owned_groups(account_data['id']))

        input(middle_text(f"{Color(139, 59, 217)}Ready to scan {len(groups)} groups! {Color(255, 255, 255)}Press Enter to begin!", 50))
        for group in groups:
            funds, pending = asyncio.run(get_group_robux(group['id'], mode, show_ratelimit))
            total_pending += pending
            total_funds += funds

            messages = []

            if mode == "full":
                if funds == 0 and pending == 0:
                    if showing_0_robux:
                        messages.append(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Funds: {Color(255, 255, 255)}0 {Color(142, 66, 214)}Pending: {Color(255, 255, 255)}0")
                else:
                    messages.append(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Funds: {Color(255, 255, 255)}{funds} {Color(142, 66, 214)}Pending: {Color(255, 255, 255)}{pending}")
            elif mode == "pending":
                if pending == 0:
                    if showing_0_robux:
                        messages.append(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Pending: {Color(255, 255, 255)}{pending}")
                else:
                    messages.append(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Pending: {Color(255, 255, 255)}{pending}")
            else:
                if funds == 0:
                    if showing_0_robux:
                        messages.append(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Funds: {Color(255, 255, 255)}{funds}")
                else:
                    messages.append(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Funds: {Color(255, 255, 255)}{funds}")

            for message in messages:
                print(middle_text(message, 50))
        print(f"{Color(142, 66, 214)}[ Total ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Funds: {Color(255, 255, 255)}{total_funds} {Color(142, 66, 214)}Pending: {Color(255, 255, 255)}{total_pending}")
        print(F"{Color(139, 59, 217)}Succesfully scanned {len(groups)} group! {Color(255, 255, 255)}Press Enter to exit.")
        os.system("title mehhovcki - group checker v1")

#### REQUESTS
async def get_account_data() -> dict:
    new_current_cookie = current_cookie
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": new_current_cookie}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}


        except Exception as e:
            print(middle_text(f"{Color(158, 105, 209)}Error occured! {Color(255, 255, 255)}While getting user data, we experienced error. Trying again in 2 seconds...", 10))

    await asyncio.sleep(2)
    return await get_account_data()

async def get_owned_groups(user_id: int) -> list:
    new_current_cookie = current_cookie
    groups: list = []

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles?includeLocked=false", cookies={".ROBLOSECURITY": new_current_cookie}) as response:
                if response.status == 200:
                    json = await response.json()

                    for group in json["data"]:
                        if group["role"]["rank"] == 255:
                            groups.append({"name": group["group"]["name"], "id": group["group"]["id"]})
                    
                    return groups
        except Exception as e:
            print(middle_text(f"{Color(158, 105, 209)}Error occured! {Color(255, 255, 255)}While getting owned groups, we experienced error. Trying again in 2 seconds...", 10))
        
    await asyncio.sleep(2)
    return await get_owned_groups(user_id)

async def get_group_robux(group_id: int, mode: str, show_ratelimit: bool):
    new_current_cookie = current_cookie
    funds = pending = None
    today = datetime.now().strftime("%Y-%m-%d")

    async with aiohttp.ClientSession() as session:
        try:
            if mode == "full":
                async with session.get(f"https://economy.roblox.com/v1/groups/{group_id}/currency", cookies={".ROBLOSECURITY": new_current_cookie}) as funds_request:
                    if funds_request.status == 200:
                        if (await funds_request.json()).get("robux") is not None:
                            funds = (await funds_request.json()).get("robux")
                    else:
                        if funds_request.status == 429:
                            if show_ratelimit:
                                print(middle_text(f"{Color(255, 255, 255)}Encountered ratelimit! Sleeping for 60 seconds", width))
                            await asyncio.sleep(60)
                            return await get_group_robux(group_id, mode, show_ratelimit)
                
                async with session.get(f"https://economy.roblox.com/v1/groups/{group_id}/revenue/summary/{today}", cookies={".ROBLOSECURITY": new_current_cookie}) as pending_request:
                    if pending_request.status == 200:
                        if (await pending_request.json()).get("pending") is not None:
                            pending = (await pending_request.json()).get("pending")
                    else:
                        if pending_request.status == 429:
                            if show_ratelimit:
                                print(middle_text(f"{Color(255, 255, 255)}Encountered ratelimit! Sleeping for 60 seconds", width))
                            await asyncio.sleep(60)
                            return await get_group_robux(group_id, mode, show_ratelimit)
            elif mode == "pending":
                async with session.get(f"https://economy.roblox.com/v1/groups/{group_id}/revenue/summary/{today}", cookies={".ROBLOSECURITY": new_current_cookie}) as pending_request:
                    if pending_request.status == 200:
                        if (await pending_request.json()).get("pending") is not None:
                            pending = (await pending_request.json()).get("pending")
                    else:
                        if pending_request.status == 429:
                            if show_ratelimit:
                                print(middle_text(f"{Color(255, 255, 255)}Encountered ratelimit! Sleeping for 60 seconds", width))
                            await asyncio.sleep(60)
                            return await get_group_robux(group_id, mode, show_ratelimit)
            elif mode == "funds":
                async with session.get(f"https://economy.roblox.com/v1/groups/{group_id}/currency", cookies={".ROBLOSECURITY": new_current_cookie}) as funds_request:
                    if funds_request.status == 200:
                        if (await funds_request.json()).get("robux") is not None:
                            funds = (await funds_request.json()).get("robux")
                    else:
                        if funds_request.status == 429:
                            if show_ratelimit:
                                print(middle_text(f"{Color(255, 255, 255)}Encountered ratelimit! Sleeping for 60 seconds", width))
                            await asyncio.sleep(60)
                            return await get_group_robux(group_id, mode, show_ratelimit)
            else:
                print(middle_text(f"{Color(255, 50, 50)}Something interesting. Encountered mode, that is not in ['funds', 'pending', 'full'] list. Maybe don't modify files? :D", 20))
        except Exception as e:
            print(middle_text(f"{Color(158, 105, 209)}Error occured! {Color(255, 255, 255)}While getting group robux data, we experienced error. Trying again in 2 seconds...", 10))
            await asyncio.sleep(2)
            return await get_group_robux(group_id, mode, show_ratelimit)
    
    return funds or 0, pending or 0

async def make_funds_visible(group_id: int, validation_token: str):
    new_current_cookie = current_cookie

    json: dict = {"areGroupFundsVisible": True}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(f"https://groups.roblox.com/v1/groups/{group_id}/settings", cookies={".ROBLOSECURITY": new_current_cookie}, json=json, headers={"x-csrf-token": validation_token}) as response:
                if response.status == 200:
                    return {}
                else:
                    return await response.json()

        except Exception as e:
            print(middle_text(f"{Color(158, 105, 209)}Error occured! {Color(255, 255, 255)}While making funds visible, we experienced error. Trying again in 2 seconds...", 10))
        
        await asyncio.sleep(2)
        return await make_funds_visible(group_id)

async def public_shout(group_id: int, validation_token: str, shout: str):
    new_current_cookie = current_cookie

    json: dict = {"message": shout}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(f"https://groups.roblox.com/v1/groups/{group_id}/status", cookies={".ROBLOSECURITY": new_current_cookie}, json=json, headers={"x-csrf-token": validation_token}) as response:
                if response.status == 200:
                    return {}
                else:
                    return await response.json()
        except Exception as e:
            print(middle_text(f"{Color(158, 105, 209)}Error occured! {Color(255, 255, 255)}While making funds visible, we experienced error. Trying again in 2 seconds...", 10))
        
        await asyncio.sleep(2)
        return await public_shout(group_id, validation_token, shout)

async def token_validator():
    new_current_cookie = current_cookie
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("https://catalog.roblox.com/", cookies={".ROBLOSECURITY": new_current_cookie}) as response:
                if response.headers.get("x-csrf-token") is not None:
                    return response.headers.get("x-csrf-token")
                else:
                    return None
        except Exception as e:
            print(middle_text(f"{Color(158, 105, 209)}Error occured! {Color(255, 255, 255)}While validating token, we experienced error. Trying again in 2 seconds...", 10))
        
        await asyncio.sleep(2)
        return await token_validator()

def save_cookie(cookie: str):
    with open("cookie.txt", "a") as file: file.close() # to make sure it even exists
    with open("cookie.txt", "w") as file: file.write(cookie)

#### CODE
while True:
    try:
        gradient_print(c, start_color="#af95c9", end_color="#5d07a3")
        # print(middle_text(f"{Color(139, 59, 217)}0 {Color(255, 255, 255)}- Exit                           {Color(112, 46, 176)}| This feature exists only if you are lazy to close cmd, or press CTRL+C", 10))
        if current_cookie != "":
            print(middle_text(f"{Color(176, 107, 242)}You have attached your Roblox Cookie!", width))
        print(middle_text(f"{Color(139, 59, 217)}0 {Color(255, 255, 255)}- Exit                           {Color(112, 46, 176)}| This feature exists only if you are lazy to close cmd, or press CTRL+D", 10))
        print(middle_text(f"{Color(139, 59, 217)}1 {Color(255, 255, 255)}- Add Cookie                     {Color(112, 46, 176)}| Add Roblox Cookie to Group scanner. Required to setup in order to have everything work.", 10))
        print(middle_text(f"{Color(139, 59, 217)}2 {Color(255, 255, 255)}- Create full Scan               {Color(112, 46, 176)}| Full scan, including check for Pending and Funds.", 10))
        print(middle_text(f"{Color(139, 59, 217)}3 {Color(255, 255, 255)}- Create Scan for Pending        {Color(112, 46, 176)}| Checks only for pending. Way faster, than full scan.", 10))
        print(middle_text(f"{Color(139, 59, 217)}4 {Color(255, 255, 255)}- Create Scan for Funds          {Color(112, 46, 176)}| Checks only for funds. Way faster, than full scan.", 10))
        print(middle_text(f"{Color(139, 59, 217)}5 {Color(255, 255, 255)}- Mass Funds Visibility          {Color(112, 46, 176)}| Makes all owned group funds visible for everyone.", 10))
        print(middle_text(f"{Color(139, 59, 217)}6 {Color(255, 255, 255)}- Mass Group Shout Changer       {Color(112, 46, 176)}| Changes shouts of all owned groups to setted one.", 10))


        print("\n\n")
        choice = input(middle_text(f"{Color(139, 59, 217)}> {Color(255, 255, 255)}", 50))

        if choice not in ["0", "1", "2", "3", "4", "5", "6"]:
            print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Invalid Choice. Press Enter to continue.", 50))
        else:
            try:
                if choice == "0":
                    input(F"{Color(139, 59, 217)}Thank you for using! {Color(255, 255, 255)}Press Enter to exit.")
                    exit(0)

                if choice == "1":
                    os.system("cls")
                    os.system("title enter your cookie - mehhovcki - group checker v1")

                    if current_cookie == "":
                        pass
                    else:
                        print(middle_text(f"{Color(139, 59, 217)}You have already setted your cookie: {Color(255, 255, 255)}{current_cookie[:150]}", 50))
                        print("\n")

                    print(middle_text(f"{Color(255, 255, 255)}You need to enter your Roblox Cookie in the input, then press Enter in order to save it.", 50))
                    print(middle_text(f"If you will have empty input, it will ask you once again to enter your cookie. Enter 'nil' to exit. {Color(139, 59, 217)}", 50))

                    while True:
                        cookie = input(middle_text(f"{Color(139, 59, 217)}> {Color(255, 255, 255)}", 50))
                        if cookie == "nil":
                            print(middle_text(f"{Color(139, 59, 217)}Exited! {Color(255, 255, 255)}Press Enter to continue.", 50))
                            os.system("title mehhovcki - group checker v1")
                            break
                        elif cookie == "":
                            continue
                        else:
                            if cookie.startswith("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"):
                                current_cookie = cookie
                                save_cookie(cookie)
                                print(middle_text(f"{Color(139, 59, 217)}Updated! {Color(255, 255, 255)}Press Enter to continue.", 50))
                                break
                            else:
                                print(middle_text(f"{Color(255, 255, 255)}You need to enter valid Roblox Cookie in the input.", 50))

                if choice == "2":
                    if current_cookie == "": print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}You need to set your cookie first. Press Enter to continue.", 50))
                    else: handle_with_scans("full")

                elif choice == "3":
                    if current_cookie == "": print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Cookie was not found. Try new cookie next time. Press Enter to continue.", 50))
                    else: handle_with_scans("pending")
                
                elif choice == "4":
                    if current_cookie == "": print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Cookie was not found. Try new cookie next time. Press Enter to continue.", 50))
                    else: handle_with_scans("funds")
                
                elif choice == "5":
                    if current_cookie == "": print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Cookie was not found. Try new cookie next time. Press Enter to continue.", 50))
                    else:
                        os.system(f"title funds visibility - mehhovcki - group checker v1")
                        print(middle_text(f"{Color(139, 59, 217)}Getting account data... {Color(255, 255, 255)}Please, wait a little..", 50))
                        account_data: dict = asyncio.run(get_account_data())
                        print(middle_text(f"{Color(139, 59, 217)}Getting validation token... {Color(255, 255, 255)}Please, wait a little..", 50))
                        x_token: str = asyncio.run(token_validator())
                        if x_token != None:
                            print(middle_text(f"{Color(139, 59, 217)}Account data was found! {Color(255, 255, 255)}Starting full scan on {account_data['name']} ({account_data['displayName']}).", 50))
                            groups: list = asyncio.run(get_owned_groups(account_data['id']))

                            input(middle_text(f"{Color(139, 59, 217)}Ready to make {len(groups)} groups funds visible! {Color(255, 255, 255)}Press Enter to begin!", 50))
                            for group in groups:
                                response = asyncio.run(make_funds_visible(group['id'], x_token))
                                if response == {}:
                                    print(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Visibility: {Color(255, 255, 255)}Enabled")
                                else:
                                    print(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Visibility: {Color(255, 255, 255)}Failed")
                            
                            print(middle_text(f"{Color(139, 59, 217)}Finished! {Color(255, 255, 255)}Press Enter to continue.", 50))
                        else:
                            print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Account validation token failed to load. Maybe account glitched?. Press Enter to continue.", 50))
                        os.system(f"title mehhovcki - group checker v1")

                elif choice == "6":
                    if current_cookie == "": print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Cookie was not found. Try new cookie next time. Press Enter to continue.", 50))
                    else:
                        os.system(f"title shout changer - mehhovcki - group checker v1")
                        print(middle_text(f"{Color(139, 59, 217)}Getting account data... {Color(255, 255, 255)}Please, wait a little..", 50))
                        account_data: dict = asyncio.run(get_account_data())
                        print(middle_text(f"{Color(139, 59, 217)}Getting validation token... {Color(255, 255, 255)}Please, wait a little..", 50))
                        x_token: str = asyncio.run(token_validator())
                        if x_token != None:
                            print(middle_text(f"{Color(139, 59, 217)}Account data was found! {Color(255, 255, 255)}Starting full scan on {account_data['name']} ({account_data['displayName']}).", 50))
                            groups: list = asyncio.run(get_owned_groups(account_data['id']))

                            print(middle_text(f"Please, enter valid shout text. It's going to be used to publish in groups, so you decide what its going to be.", 50))
                            new_choice = input(middle_text(f"{Color(139, 59, 217)}> {Color(255, 255, 255)}", 50))

                            shout_text: str = new_choice

                            input(middle_text(f"{Color(139, 59, 217)}Ready to make {len(groups)} groups shout visible! {Color(255, 255, 255)}Press Enter to begin!", 50))
                            for group in groups:
                                response = asyncio.run(public_shout(group['id'], x_token, shout_text))

                                if response == {}:
                                    print(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Shout: {Color(255, 255, 255)}Success")
                                else:
                                    print(f"{Color(142, 66, 214)}[ {group['name']} ({group['id']}) ] {Color(255, 255, 255)} >>> {Color(142, 66, 214)}Shout: {Color(255, 255, 255)}Failed {response}")
                            
                            print(middle_text(f"{Color(139, 59, 217)}Finished! {Color(255, 255, 255)}Press Enter to continue.", 50))
                        else:
                            print(middle_text(f"{Color(139, 59, 217)}Error: {Color(255, 255, 255)}Account validation token failed to load. Maybe account glitched?. Press Enter to continue.", 50))
                        os.system(f"title mehhovcki - group checker v1")    
            except KeyboardInterrupt:
                print("\n")
                print(middle_text(f"{Color(139, 59, 217)}Force-Exit! {Color(255, 255, 255)}Press Enter to continue.", 50))
                os.system(f"title mehhovcki - group checker v1")


        input("")
        if os.system("nt"): os.system("cls")
        else: os.system("clear")
    except KeyboardInterrupt:
        exit(0)
