import React, { Component } from 'react'
import {Paper, Typography} from '@material-ui/core';

import './style.css'
export default class Message extends Component {

    formatAlign(align){
        if(align === 'left') {
            return 'flex-start'
        }
        if(align === 'right') {
            return 'flex-end'
        }
        return 'flex-end'
    }
    
    render() {
        const OneMessageStyle = {
            background: this.props.isBot?'#ecf0f1':'#2e86de',
            color: this.props.isBot?'black' :'white'
        }
        return (
            <div className="Message" style={{alignSelf:this.formatAlign(this.props.align)}}>
               <Paper className="OneMessage" style={OneMessageStyle}>
                    <div className="MessageContent">
                        <Typography component="p">
                           {this.props.content}
                        </Typography>
                    </div>
                </Paper>
            </div>
        )
    }
}
