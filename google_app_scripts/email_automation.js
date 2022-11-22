var EMAIL_TEMPLATE_DOC_URL =
  "https://docs.google.com/document/d/xxx/edit?usp=sharing";
var EMAIL_SUBJECT = "Welcome to X";

// Installs a trigger on the Spreadsheet for when a Form response is submitted.
function installTrigger() {
  ScriptApp.newTrigger("onFormSubmit")
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onFormSubmit()
    .create();
}

/**
 * Sends a customized email for every response on a form.
 *
 * @param {Object} event - Form submit event
 */
function onFormSubmit(e) {
  var responses = e.namedValues;

  var htmlBody = "<ul>";
  for (Key in responses) {
    var label = Key;
    var data = responses[Key];
    htmlBody += "<li>" + label + ": " + data + "</li>";
  }
  htmlBody += "</ul>";
  GmailApp.sendEmail(
    "client@domain.com",
    "Email Body",
    "",
    { htmlBody: htmlBody }
  );
  var timestamp = responses.Timestamp[0];
  var email = responses["Email Address"][0].trim();
  var name = responses["First Name"][0].trim();
  MailApp.sendEmail({
    to: email,
    subject: EMAIL_SUBJECT,
    htmlBody: createEmailBody(name),
  });
  status = "Sent";

  // Append the status on the spreadsheet to the responses' row.
  var sheet = SpreadsheetApp.getActiveSheet();
  var row = sheet.getActiveRange().getRow();
  var column = e.values.length + 1;
  sheet.getRange(row, column).setValue(status);

  Logger.log("status=" + status + "; responses=" + JSON.stringify(responses));
}

/**
 * Creates email body and includes the links based on topic.
 *
 * @param {string} recipient - The recipient's email address.
 * @param {string[]} topics - List of topics to include in the email body.
 * @return {string} - The email body as an HTML string.
 */
function createEmailBody(name) {
  // Make sure to update the emailTemplateDocId at the top.
  var docId = DocumentApp.openByUrl(EMAIL_TEMPLATE_DOC_URL).getId();
  var emailBody = docToHtml(docId);
  emailBody = emailBody.replace(/{{NAME}}/g, name);
  return emailBody;
}

/**
 * Downloads a Google Doc as an HTML string.
 *
 * @param {string} docId - The ID of a Google Doc to fetch content from.
 * @return {string} The Google Doc rendered as an HTML string.
 */
function docToHtml(docId) {
  // Downloads a Google Doc as an HTML string.
  var url =
    "https://docs.google.com/feeds/download/documents/export/Export?id=" +
    docId +
    "&exportFormat=html";
  var param = {
    method: "get",
    headers: { Authorization: "Bearer " + ScriptApp.getOAuthToken() },
    muteHttpExceptions: true,
  };
  return UrlFetchApp.fetch(url, param).getContentText();
}
