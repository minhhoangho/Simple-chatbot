import React, {Component} from 'react';
import Message from "../Message";
import './style.css'

export default class MessageList extends Component {

    constructor(props) {
        super(props)
        this.state = {
            msgList: null
        }
    }

    scrollToBottom = () => {
        this
            .messagesEnd
            .scrollIntoView();
    }
    
    async componentDidUpdate() {
        setTimeout(()=>{
            console.log("Waiting for render message") 
        }, 750)
        const res = await fetch('http://localhost:5000/api/v1/messages');
        const data = await res.json()
        this.setState({msgList: data.results})
        this.scrollToBottom();
    }
    async componentDidMount() {
        const res = await fetch('http://localhost:5000/api/v1/messages');
        const data = await res.json()
        this.setState({msgList: data.results})
        this.scrollToBottom();
    }

    render() {
        return (
            <div className="MessageContainer">
                <div className="MessageList">
                    {this.state.msgList
                        ? this
                            .state
                            .msgList
                            .map((e, idx) => {
                                const align = (e.isBot === true)
                                    ? 'left'
                                    : 'right'
                                return (<Message key={idx} isBot={e.isBot} align={align} content={e.content}/>)
                            })
                        : null
}
                    <div
                        style={{
                        float: "left",
                        clear: "both"
                    }}
                        ref={(el) => {
                        this.messagesEnd = el;
                    }}></div>
                </div>

            </div>

        );
    }

}
