import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtMultimedia 5.8

Window {
    id: root
    visible: true
    width: 800; height: 400
    color: "#aaa"
    title: qsTr("Recorder")

    property bool validation: false
    property bool recording: false
    property string promptsName: ''
    property string promptTitle: ''
    property string scriptText: ''
    property string scriptFilename: ''
    property string saveDir: '.'

    Component.onCompleted: initTimer.start()
    Timer {
        id: initTimer
        interval: 0
        onTriggered: recorder.init(scriptModel)
    }

    onRecordingChanged: recorder.toggleRecording(recording)
    onScriptFilenameChanged: scriptModel.get(scriptListView.currentIndex).filename = scriptFilename

    function appendScript(data) {
        scriptModel.append(data)
    }

    function gotoPreviousScript() {
        scriptListView.decrementCurrentIndex();
        scriptListView.positionViewAtIndex(scriptListView.currentIndex, ListView.Center);
    }

    function gotoNextScript() {
        scriptListView.incrementCurrentIndex();
        scriptListView.positionViewAtIndex(scriptListView.currentIndex, ListView.Center);
    }

    function setTitle() {
        title: qsTr("Validator")
    }

    ListModel {
        id: scriptModel
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 6

        Frame {
            Layout.fillHeight: true
            Layout.fillWidth: true
            focus: true

            ListView {
                id: scriptListView
                model: scriptModel
                anchors.fill: parent
                focus: true
                clip: true
                ScrollBar.vertical: ScrollBar { active: true; policy: ScrollBar.AlwaysOn }
                highlight: Rectangle { color: "lightsteelblue"; radius: 5 }

                onCurrentItemChanged: {
                    scriptText = model.get(currentIndex).script;
                    scriptFilename = model.get(currentIndex).filename;
                    console.log('selected: "' + scriptText + '", ' + scriptFilename);
                }

                delegate: Item {
                    width: parent.width - 20
                    height: 30
                    Column {
                        Text {
                            text: script
                            font.pointSize: 10
                        }
                        Text {
                            text: 'Filename: ' + filename
                            font.pointSize: 8
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: scriptListView.currentIndex = index
                    }
                }
            }
        }

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width
            height: parent.height
            color: validation ? "#7C0A02" : "#fff"
            font.pixelSize: 20
            text: validation ? "Validation View -> " + promptTitle : "Recording View -> " + promptTitle
        }

        CheckBox {
            Layout.fillWidth: true
            font.pointSize: 14
            text: 'Filter all punctuation (only speak normal words!)'
            checked: true
            enabled: false
        }

        TextArea {
            Layout.fillWidth: true
            font.pointSize: 14
            wrapMode: TextEdit.Wrap
            readOnly: true
            text: scriptText
            background: Rectangle {
                border.width: 3
                border.color: recording ? "#2b2" : "#b22"
            }
        }

        Button {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            font.pointSize: 16
            highlighted: recording
            text: recording ? "Stop" : "Start"
            focusPolicy: Qt.NoFocus
            onClicked: {
                recording = !recording;
                if (recording) {
                    recorder.startRecording();
                } else {
                    recorder.finishRecording();
                    gotoNextScript();
                }
            }
        }

        RowLayout {
            Button {
                Layout.fillWidth: true
                font.pointSize: 14
                text: "Play"
                focusPolicy: Qt.NoFocus
                enabled: scriptFilename
                highlighted: playFile.playbackState == playFile.PlayingState
                // onClicked: recorder.playFile(scriptFilename)
                onClicked: {
                    playFile.source = scriptFilename
                    playFile.play()
                }
                Audio {
                    id: playFile
                    source: ''
                }
            }

            Button {
                Layout.fillWidth: true
                font.pointSize: 14
                text: "Delete"
                focusPolicy: Qt.NoFocus
                enabled: scriptFilename
                onClicked: recorder.deleteFile(scriptFilename)
            }

            Button {
                Layout.fillWidth: true
                font.pointSize: 14
                text: recording ? "Cancel" : "Next"
                focusPolicy: Qt.NoFocus
                onClicked: {
                    if (recording) {
                        recording = !recording;
                    } else {
                        gotoNextScript()
                    }
                }
            }
        }
    }

}
