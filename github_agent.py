import asyncio
import os
import traceback
import streamlit as st
from textwrap import dedent
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

st.set_page_config(page_title="🚀 GitScope", page_icon="🚀", layout="wide")

st.markdown(
    '<h1 style="text-align:center; font-size:48px;">🚀 GitScope</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align:center; color:#aaa; margin-bottom:10px;">Analyze GitHub repositories with MCP-powered AI insights</p>',
    unsafe_allow_html=True,
)

st.markdown("""
<div style="text-align:center; margin:30px 0;">
  <img src="https://cdn.dribbble.com/users/1162077/screenshots/3848914/programmer.gif"
       width="200"
       style="border-radius:10px; animation: float 3s ease-in-out infinite;" />
</div>

<style>
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}
</style>
""", unsafe_allow_html=True)

if not os.getenv("GITHUB_TOKEN"):
    st.warning("⚠️ Set GITHUB_TOKEN in terminal")

repo = st.text_input("Repository", value="vercel/next.js")

if repo.startswith("https://github.com/"):
    repo = repo.replace("https://github.com/", "").strip("/")

mode = st.radio(
    "Analysis Mode",
    ["Repo Health", "PR Summary", "Bug Triage"],
    horizontal=True
)

if mode == "Repo Health":
    default_query = f"Analyze repository health and activity in {repo}"
elif mode == "PR Summary":
    default_query = f"Summarize recent pull requests in {repo}"
else:
    default_query = f"Find important bugs and issue trends in {repo}"

query = st.text_area("Your Query", value=default_query, height=140)

async def run_github_agent(message: str):
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            return "Error: GITHUB_TOKEN is not set."

        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={**os.environ, "GITHUB_TOKEN": github_token},
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                mcp_tools = MCPTools(session=session)
                await mcp_tools.initialize()

                agent = Agent(
                    tools=[mcp_tools],
                    instructions=dedent("""
                    You are a GitHub repository analyst.

                    Always structure your answer like this:
                    1. Executive Summary
                    2. Key Findings
                    3. Risks / Concerns
                    4. Recommended Actions

                    Keep it concise and clear.
                    Base everything on GitHub data.
                    """),
                    markdown=True,
                )

                response = await agent.arun(message)
                return response.content if hasattr(response, "content") else str(response)

    except BaseException as e:
        return f"Error: {type(e).__name__}: {e}\n\nTraceback:\n{traceback.format_exc()}"

run = st.button("🚀 Run Analysis")

if run:
    result = asyncio.run(run_github_agent(query))
    st.markdown(f"## 📊 Results for `{repo}`")
    st.markdown(result)

st.markdown("---")
st.write("Built with Streamlit and MCP ❤️")
