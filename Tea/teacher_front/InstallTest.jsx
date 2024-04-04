const React = require('react');
const { Component } = React;

class InstallTest extends Component {
	state = {
    	text : '성공적인 웹팩 설치! 😊',
    };
    
    render(){
    	return <h1>{this.state.text}</h1>
    }
}

module.exports = InstallTest;