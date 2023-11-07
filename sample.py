package com.abhijeetofspades.chatbot;

import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;

import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.res.AssetManager;
import android.net.Uri;
import android.os.Environment;
import android.speech.RecognizerIntent;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.TextInputEditText;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import org.alicebot.ab.AIMLProcessor;
import org.alicebot.ab.Bot;
import org.alicebot.ab.Chat;
import org.alicebot.ab.Graphmaster;
import org.alicebot.ab.MagicBooleans;
import org.alicebot.ab.MagicStrings;
import org.alicebot.ab.PCAIMLProcessorExtension;
import org.alicebot.ab.Timer;
import com.abhijeetofspades.chatbot.Adapter.ChatMessageAdapter;
import com.abhijeetofspades.chatbot.Pojo.ChatMessage;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

private ListView mListView;
private FloatingActionButton mButtonSend;
private EditText txvResult;
private ImageView mImageView;
public Bot bot;
public static Chat chat;
private ChatMessageAdapter mAdapter;
private EditText query;
private EditText escapedQuery;

@Override
protected void onCreate(Bundle savedInstanceState) {
super.onCreate(savedInstanceState);
setContentView(R.layout.activity_main);
mListView = (ListView) findViewById(R.id.listView);
mButtonSend = (FloatingActionButton) findViewById(R.id.btn_send);
txvResult = (EditText) findViewById(R.id.txvResult);
mImageView = (ImageView) findViewById(R.id.iv_image);
mAdapter = new ChatMessageAdapter(this, new ArrayList<ChatMessage>());
mListView.setAdapter(mAdapter);
mButtonSend.setOnClickListener(new View.OnClickListener() {
@Override
public void onClick(View v) {
String message = txvResult.getText().toString();
*//startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://www.google.com/search?q="+message)));

//bot

String response = chat.multisentenceRespond(txvResult.getText().toString());
if (TextUtils.isEmpty(message)) {
return;
}
sendMessage(message);
mimicOtherMessage(response);
txvResult.setText("");
mListView.setSelection(mAdapter.getCount() - 1);
}
});
*//checking SD card availablility
boolean a = isSDCARDAvailable();
*//receiving the assets from the app directory
AssetManager assets = getResources().getAssets();
File jayDir = new File(Environment.getExternalStorageDirectory().toString() + "/abhijeet/bots/Abhijeet");
boolean b = jayDir.mkdirs();
if (jayDir.exists()) {
*//Reading the file
try {
for (String dir : assets.list("Abhijeet")) {
File subdir = new File(jayDir.getPath() + "/" + dir);
boolean subdir_check = subdir.mkdirs();
for (String file : assets.list("Abhijeet/" + dir)) {
File f = new File(jayDir.getPath() + "/" + dir + "/" + file);
if (f.exists()) {
continue;
}
InputStream in = null;
OutputStream out = null;
in = assets.open("Abhijeet/" + dir + "/" + file);
out = new FileOutputStream(jayDir.getPath() + "/" + dir + "/" + file);
*//copy file from assets to the mobile's SD card or any secondary memory
copyFile(in, out);
in.close();
in = null;
out.flush();
out.close();
out = null;
}
}
} catch (IOException e) {
e.printStackTrace();
}
}
*//get the working directory
MagicStrings.root_path = Environment.getExternalStorageDirectory().toString() + "/abhijeet";
System.out.println("Working Directory = " + MagicStrings.root_path);
AIMLProcessor.extension = new PCAIMLProcessorExtension();
*//Assign the AIML files to bot for processing
bot = new Bot("Abhijeet", MagicStrings.root_path, "chat");
chat = new Chat(bot);
String[] args = null;
mainFunction(args);
}

public void getSpeechInput(View view) {
Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH);
intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
startActivityForResult(intent, 10);

}

@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
super.onActivityResult(requestCode, resultCode, data);

switch (requestCode) {
case 10:
if (resultCode == RESULT_OK && data != null) {
ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
txvResult.setText(result.get(0));
}
break;
}
}

private void sendMessage(String message) {
ChatMessage chatMessage = new ChatMessage(message, true, false);
mAdapter.add(chatMessage);

*//mimicOtherMessage(message);

}
private void mimicOtherMessage(String message) {
ChatMessage chatMessage = new ChatMessage(message, false, false);
mAdapter.add(chatMessage);
}

private void sendMessage() {
ChatMessage chatMessage = new ChatMessage(null, true, true);
mAdapter.add(chatMessage);

mimicOtherMessage();
}

private void mimicOtherMessage() {
ChatMessage chatMessage = new ChatMessage(null, false, true);
mAdapter.add(chatMessage);
}

*//check SD card availability

public static boolean isSDCARDAvailable() {
return Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED) ? true : false;
}
*//copying the file

private void copyFile(InputStream in, OutputStream out) throws IOException {
byte[] buffer = new byte[1024];
int read;
while ((read = in.read(buffer)) != -1) {
out.write(buffer, 0, read);
}
}
*//Request and response of user and the bot

public static void mainFunction(String[] args) {
MagicBooleans.trace_mode = false;
System.out.println("trace mode = " + MagicBooleans.trace_mode);
Graphmaster.enableShortCuts = true;
Timer timer = new Timer();
String request = "Hello.";
String response = chat.multisentenceRespond(request);
System.out.println("Human: " + request);
System.out.println("Robot: " + response);

}

}
