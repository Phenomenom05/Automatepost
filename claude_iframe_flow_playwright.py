
import time

from playwright.sync_api import sync_playwright, TimeoutError

TARGET_URL = "https://claude.ai/public/artifacts/3e407d20-4645-42a0-b1ba-b3636087f841"



def attach_to_artifact_frame(page, timeout=20_000):

    deadline = time.time() + timeout / 1000.0
    while time.time() < deadline:
        try:
            # Re-fetch frames each loop to avoid "frame detached" issues
            for frame in page.frames:
                try:
                    # fast checks for known markers inside iframe
                    # note: count() is safe here because we are re-querying the frames list
                    if frame.locator("#artifacts-component-root-html").count() > 0:
                        return frame
                    if frame.locator("#newTitle").count() > 0:
                        return frame
                    if frame.locator("button:has-text('Create Post')").count() > 0:
                        return frame
                except Exception:
                    # Locator calls can throw if a frame is mid-reload — ignore and continue
                    continue
        except Exception:
            pass
        time.sleep(0.5)
    return None


def perform_flow(page):
    print("▶ Navigating to target URL ...")
    page.goto(TARGET_URL, timeout=60_000)
    print("Page loaded. Waiting for iframe / potential Cloudflare challenge...")

    # short wait to allow Cloudflare to appear if it will
    time.sleep(2)

    # Attach to the artifact iframe
    frame = attach_to_artifact_frame(page, timeout=15_000)
    if frame is None:
        # Fallback: ask user to manually solve any presented challenge in the opened browser
        print("Cloudflare challenge may be present or artifact iframe not yet mounted.")
        print("Please inspect the opened browser window. If a CAPTCHA/challenge appears, solve it manually.")
        input("After you've solved the challenge (or if none appeared), press Enter to continue...")
        # Retry attaching to iframe after manual solve
        frame = attach_to_artifact_frame(page, timeout=30_000)
        if frame is None:
            raise RuntimeError("Could not find the artifact iframe after manual solve. Inspect browser and try again.")

    print("[info] Attached to artifacts iframe ✅")

    # Wait for Create Post tab/button and click it
    try:
        # Wait until a button with text 'Create Post' is visible inside the frame
        create_btn = frame.locator("button:has-text('Create Post')")
        create_btn.first.wait_for(state="visible", timeout=12_000)
        create_btn.first.click()
        print("🖱 Clicked Create Post tab/button.")
    except TimeoutError:
        print("Error")
        # fallback: try clicking the third tab button (.tabs .tab)



    # Wait for form fields to appear and fill them
    title = frame.locator("#newTitle")
    content = frame.locator("#newContent")
    author_select = frame.locator("#newAuthor")

    title.wait_for(state="visible", timeout=10_000)
    content.wait_for(state="visible", timeout=10_000)
    author_select.wait_for(state="visible", timeout=10_000)

    title.fill("Test Title")
    content.fill("Test Content")
    frame.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # select a valid author option
    options = author_select.locator("option")
    opt_count = options.count()
    selected = False
    for i in range(opt_count):
        try:
            v = options.nth(i).get_attribute("value") or ""
            if v.strip():
                author_select.select_option(value=v)
                selected = True
                break
        except Exception:
            continue
    if not selected and opt_count > 1:
        try:
            fallback_v = options.nth(1).get_attribute("value")
            if fallback_v:
                author_select.select_option(value=fallback_v)
                selected = True
        except Exception:
            pass

    print("✅ Form fields filled.")


    # Click the Create Post button
    submit_btn = frame.locator("button.btn:has-text('Create Post')")
    submit_btn.first.click()

    # Scroll to the top of the page and wait for visibility of the Dashboard button
    frame.evaluate("window.scrollTo(0, 0)")
    time.sleep(5)
    dashboard_btn = frame.locator("button.tab:has-text('Dashboard')")
    dashboard_btn.scroll_into_view_if_needed(timeout=5000)
    dashboard_btn.wait_for(state="visible", timeout=10_000)
    dashboard_btn.click()


# Check the post Count
    pc = frame.locator("#postCount").inner_text()
    print("📊 postCount:", pc)


    time.sleep(5)
    # Scroll to the bottom of the page
    frame.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    # Get the title and content of the newly created post
    title_text = frame.locator("h3:has-text('Test Title')")
    content_text = frame.locator("p:has-text('Test Content')")
    if title_text.count() > 0:
        print("Test was successful.")
        # Print the new post title
        print("Test  Title is : " +  title_text.first.inner_text())
        #Print the new post content
        print("Test  Content is : " + content_text.first.inner_text())
    else:
        print("Test was not successful.")








def main():
    # # Ensure the user_data_dir path exists (Playwright will create if missing)
    # ud = Path(USER_DATA_DIR)
    # ud.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-first-run",
                "--no-default-browser-check",
            ]
        )

        page = browser.new_page(viewport={"width": 1115, "height": 663})

        # open a new page (tab) in persistent context

        try:
            perform_flow(page)
            input("Flow finished. Press Enter to close browser...")
        except Exception as e:
            print("ERROR during automation:", e)
            input("Press Enter to close browser for debugging (leave window open to inspect)...")
        finally:
            try:
                browser.close()
            except Exception:
                pass


if __name__ == "__main__":

    main()
