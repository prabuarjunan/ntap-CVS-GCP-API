const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["/Users/arjunan/PycharmProjects/ntap-CVS-GCP-API/get_token.py"]);

pythonProcess.stdout.on('token', (get_token) => {
  console.log('stdout: ${get_token}');
});
pythonProcess.stdout.on('data', (data) => {
  // Do something with the data returned from python script
});