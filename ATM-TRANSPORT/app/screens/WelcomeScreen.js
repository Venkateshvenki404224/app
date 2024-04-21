import React from 'react';
import { Image, ImageBackground, StyleSheet, Text, View } from 'react-native';

function WelcomeScreen(props) {
    return (
        <ImageBackground
            style={styles.background} // 1x1 pixel transparent image
            source={require("../assets/background.png")}
        >
            <View style={styles.logoContainer}>
                <Image style={styles.logo} source={require("../assets/logo.png")} />
                <Text style={styles.font}>Effortless House Shifting and Goods Transportation Across Bangalore and Tamil Nadu</Text>
            </View>
            <View style={styles.loginButton}></View>
            <View style={styles.registerButton}></View>
        </ImageBackground>
    );
}

const styles = StyleSheet.create({
    background: {
        flex: 1,
        justifyContent: "flex-end",
        alignItems: "center",
    },
    loginButton: {
        width: '100%',
        height: 70,
        backgroundColor: '#FAC044',

    },
    registerButton: {
        width: '100%',
        height: 70,
        backgroundColor: '#F3F3F3',
    },
    logo: {
        width: 100,
        height: 100,
    },
    logoContainer: {
        position: 'absolute',
        top: 100,
        alignItems: 'center',
    },
    font: {
        fontSize: 15,
        color: 'white',
        textAlign: 'center',
        width: 300,
        marginTop: 10,
    }
})

export default WelcomeScreen;