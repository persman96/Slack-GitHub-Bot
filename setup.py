import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slack_github_bot",
    version="0.0.1",
    author="Pontus and Nikolai",
    description="Slack bot to interact with GitHub Actions",
    package_dir={"slack_github_bot": "slack_github_bot"},
    packages=["slack_github_bot"],
    package_data={'': ['config.toml']},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["flask", "slackclient", "requests", "slackeventsapi", "toml"],
)