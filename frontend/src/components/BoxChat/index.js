import React, {Component} from 'react'
import {Card, Container, Toolbar, Typography} from "@material-ui/core";
import MessageList from '../MessageList';
import SendMessageForm from '../SendMessageForm';
import './style.css'

export default class BoxChat extends Component {
    constructor(props) {
        super(props)
        this.state = {
            msg:null
        }
    }
    async getDataFromChild(msg) {
        await this.setState({
            msg:msg
        })
    }
    render() {
        return (
            <div className="BoxChat">
                <Container maxWidth="md" className="relative">
                    <div className="row">
                        <Card
                            style={{
                            "height": "100vh"
                        }}>
                            <Toolbar className="TopToolbarChatbot">
                                <Typography variant="h6" color="inherit">
                                    Chat
                                </Typography>
                            </Toolbar>
                            <MessageList newMsg={this.state.msg}/>
                            <SendMessageForm returnParent={this.getDataFromChild.bind(this)}/>
                        </Card>
                    </div>

                </Container>

            </div>
        )
    }
}
