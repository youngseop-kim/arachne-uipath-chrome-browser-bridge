
let hostName = "com.arachne.uipath.chrome.browser.bridge.host";
let host = null;
let lost = false;

let curRecursion = 0;
let maxRecursion = 30;

let curRetrial = 0;
let maxRetrial = 5;
let interval = 3000;

const sleep = (delay) => new Promise(
    (resolve, reject) => setTimeout(resolve, delay)
);

const ping = (delay) => new Promise(
    (resolve, reject) => {
        /*
        for letting the host know that the chrome-extension is alive,
        this application has to send continuos ping message every {interval} milliseconds to the host.
        the continuity of ping method will be described as an async-recursive function. 
        however, it should be stopped when the connection lost signal is detected.
        */

        // add current recursion
        curRecursion+=1;

        // send ping to let the host know the chrome-extension is alive
        sleep(delay).
            then(
                () => {
                    try {
                        // send ping message
                        host.postMessage({'key':'internal', 'value':'ping'});
                        
                        // log ping (it should be enabled only in debugging connection)
                        // console.log('ping sent.');
                    }
                    catch(e) {
                        // log ping (it should be enabled only in debugging connection)
                        console.log('ping denied.');
                    }
                }
            ).
            then(
                () => {
                    // recursion exceed max recursion
                    if(curRecursion > maxRecursion){
                        // reset current recursion
                        curRecursion = 0;
                    }
                }
            ).
            finally(
                () => {
                    if(lost) {
                        // stop recursion
                        console.log('ping stopped.')
                    }
                    else {
                        // recursion
                        ping(delay);
                    }
                }
            )
    }
); 

const connect = () => new Promise(
    (resolve, reject) => {
        // try to connect host
        // you should aware of that the exception from "chrome.runtime.connectNative" 
        // will be caught by disconnection listener, so do not try to handle exception on this method
        console.log('try to connect host...');
        host = chrome.runtime.connectNative(hostName);
        
        // this will be fired when the host connection is lost or
        // the host connection failure
        console.log(' - listen on disconnected');
        host.onDisconnect.addListener(reconnect);
        
        console.log(' - listen on message received');
        host.onMessage.addListener(inject);
    }
);

const reconnect = () => new Promise(
    (resolve, reject) => {
        // when host not found error has been occured,
        if(chrome.runtime.lastError.message == "Specified native messaging host not found.") {
            // log runtime error
            console.log('***', chrome.runtime.lastError.message, '>', curRetrial);
            
            // retry connection in interval within max retrial 
            curRetrial+=1;
            if(curRetrial<maxRetrial){
                sleep(interval).
                    then(() => connect());
            }
            else {
                lost = true;
            }
        } 

        // when uncaught runtime error has been occured,
        else {
            // log runtime error
            console.log('***', chrome.runtime.lastError.message);

            // retry connection rapidly
            curRetrial = 0;
            connect();
        }
    }
);

const queryCurrentTab = () => new Promise(
    async (resolve, reject) => {
        let [tab] = await chrome.tabs.query({active: true, currentWindow: true})
        resolve(tab)
    }
)

const inject = (message) => new Promise(
    (resolve, reject) => {
        // query current tab
        queryCurrentTab().
            then(
                // execute script javascript file
                tab => {
                    // log request message
                    console.log('requested :', message.value)

                    try {
                        // === inject javascript file on current tab & all frames ===
                        chrome.scripting.executeScript(
                            {
                                target: {tabId: tab.id, allFrames: true}, 
                                files: [message.value.replace(/\\/g, '/')]
                            },
                            (result) => {
                                // when runtime error has been occured,
                                if (chrome.runtime.lastError) {
                                    // set the runtime error message in response message
                                    message.value = chrome.runtime.lastError.message
    
                                } 
                                
                                // when javascript injection is successful,
                                else {
                                    // set the result in response message
                                    message.value = result;
                                }
                                        
                                // send response message
                                host.postMessage(message)
    
                                // log response message
                                console.log('responsed :', message.value)
                            }
                        )
                        // === inject javascript file on current tab & all frames ===
                    }
                    // when uncaught runtime error has been occured
                    catch (error) {
                        // set the runtime error message in response message as internal exception
                        message.value = '[int. exception] ' + error.message;
                                        
                        // send response message
                        host.postMessage(message)
            
                        // log response message
                        console.log('responsed :', message.value)
                    }
                }
            )
    }
);

// on browser startup
chrome.runtime.onStartup.addListener(() => connect());

// chrome-extension is started
if(host == null){
    connect()
}

// start to ping
ping(interval);