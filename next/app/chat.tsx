import { ChatWindow } from "@/components/ChatWindow";

export default function Chat() {
    return (
        <ChatWindow
        endpoint="api/chat/private"
        emoji="🏴‍☠️"
        titleText="Patchy the Chatty Pirate"
        placeholder="I'm an LLM pretending to be a pirate! Ask me about the pirate life!"
        emptyStateComponent={<></>}
      ></ChatWindow>
    )
}