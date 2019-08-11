import React, {Component} from 'react'
import {TextField} from "@material-ui/core";
// import Icon  from "@material-ui/icons";
import './style.css'
export default class SendMessageForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            message: ""
        }
        this.handleEnter = this
            .handleEnter
            .bind(this)
        this.handleSubmit = this
            .handleSubmit
            .bind(this)
        this.onChange = this
            .onChange
            .bind(this)
    }
    async handleSubmit(e) {
        e.preventDefault()
        await this.setState({
            message: this
                .state
                .message
                .replace(/(\r\n|\n|\r)/gm, "")
        })

        if (this.state.message === "") {
            return
        } else {
            fetch('http://localhost:5000/api/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json'
                },
                body: JSON.stringify({
                    content: this.state.message,
                    isBot: false,
                    time: (new Date().getTime()) / 1000
                })
            }).then(res => {
                if (res.status === 200) {
                    console.log("Send message successfully")
                    res
                        .json()
                        .then(postResponse => {
                            console.log(postResponse);
                            
                            fetch('http://localhost:5000/api/v1/messages/reply', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    Accept: 'application/json'
                                },
                                body: JSON.stringify({
                                    content: postResponse.content,
                                    isBot: false,
                                    time: (new Date().getTime()) / 1000
                                })
                            }).then(res => {
                                if (res.status === 200) {
                                    console.log("Wait for reply ...")
                                } else {
                                    console.log("Some error occured");

                                }
                            })
                        })

                } else {
                    console.log("Some error occured");
                }
            }).then(this.setState({message: ""}))

        }

    }
    handleEnter(e) {
        if (e.keyCode === 13) {
            return this.handleSubmit(e)
        }
        return
    }
    onChange(e) {
        this.setState({
            [e.target.name]: e.target.value
        });
    }
    render() {
        return (
            <div className="SendMessageForm">
                <div className="chat-input-width-100">
                    <form className="MessageForm" onKeyUp={this.handleEnter}>
                        <button className="sender" type="button" onClick={(e) => this.handleSubmit(e)}>
                            <img src="/assets/img/send-button.png" alt=""/>
                        </button>
                        <TextField
                            name="message"
                            id="outlined-multiline-static"
                            fullWidth={true}
                            multiline
                            rows="4"
                            value={this.state.message}
                            placeholder="Type something here"
                            className="chat-input"
                            margin="normal"
                            variant="outlined"
                            onChange={this.onChange}/>
                    </form>
                </div>
            </div>
        )
    }
}
