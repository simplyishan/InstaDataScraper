import instaloader
import json
import sys
# TODO: Add Discord Webhook Feature, add image feature, add search and save in sql too.
def safe_print(text):
    try:
        return text
    except UnicodeEncodeError:
        return text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)

def get_user_data():
    username = input("Enter the Instagram username: ")

    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        print("\nInstagram Profile Data:")
        print("-----------------------")
        print(f"Username: {safe_print(profile.username)}")
        print(f"Full Name: {safe_print(profile.full_name)}")
        print(f"Biography: {safe_print(profile.biography or 'No biography')}")
        print(f"Followers: {profile.followers}")
        print(f"Following: {profile.followees}")
        print(f"Posts: {profile.mediacount}")

        # Get recent posts
        print("\nRecent Posts:")
        print("--------------")
        posts = list(profile.get_posts())[:5]  # Limit to 5 recent posts
        for post in posts:
            print(f"Post: {post.url}")
            print(f"Likes: {post.likes}, Comments: {post.comments}")
            print("-" * 30)

        
        save_data = input("\nDo you want to save this data to a file? (yes/no): ").strip().lower()

        if save_data == "yes":
            filename = input("Enter the filename to save the data (e.g., 'instagram_data.json'): ")
            data = {
                "Username": profile.username,
                "Full Name": profile.full_name,
                "Biography": profile.biography or 'No biography',
                "Followers": profile.followers,
                "Following": profile.followees,
                "Posts": profile.mediacount,
                "Recent Posts": [{
                    "Post": post.url,
                    "Likes": post.likes,
                    "Comments": post.comments
                } for post in posts]
            }

            with open(filename, "w+") as file:
                json.dump(data, file, indent=4)
            print(f"Data saved to {filename}")

        else:
            print("Data not saved.")

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


get_user_data()
