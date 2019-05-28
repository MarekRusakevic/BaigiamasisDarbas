let net;
const webcamElement = document.getElementById('canvas_rez');
const classifier = knnClassifier.create();

function save(){
	
   let dataset = classifier.getClassifierDataset()
   
   console.log(dataset);
   
   var datasetObj = {}
   Object.keys(dataset).forEach((key) => {
     let data = dataset[key].dataSync();
     datasetObj[key] = Array.from(data); 
   });
   
   let jsonStr = JSON.stringify(datasetObj)
   localStorage.setItem("myData", jsonStr); 
}

function load() {
    let dataset = localStorage.getItem("myData")
    let tensorObj = JSON.parse(dataset)
	
	console.log(dataset);
	
    Object.keys(tensorObj).forEach((key) => {
		
		var len = tensorObj[key].length / 1024;
		
		tensorObj[key] = tf.tensor(tensorObj[key], [tensorObj[key].length / 1024, 1024])
		
		for(i = 0; i < len; i++){
			classifier.addExample(tf.gather(tensorObj[key], i), key);
		}
    })
}

function saveModel(){
	save();
	
	console.log('Model saved');
}

function loadModel(){
	load();
	
	console.log('Model loaded');
}

async function app() {
  console.log('Loading mobilenet..');
  // Modelio įkelimas
  net = await mobilenet.load();
  console.log('Sucessfully loaded model');
  // Nuskaito vaizdą ir asocijuoja jį su specifinės klasės indeksu
  const addExample = classId => {
	// Gauti tarpinį MobileNet 'conv_preds' aktyvavimą ir perduoti jį į
	// KNN klasifikatorių
    const activation = net.infer(webcamElement, 'conv_preds');

    classifier.addExample(activation, classId);
  };
  // Kada paspaudžiamas mygtukas, pridėti pavyzdį nurodytai klasei
  document.getElementById('class-a').addEventListener('click', () => addExample(0));
  document.getElementById('class-b').addEventListener('click', () => addExample(1));
  document.getElementById('class-c').addEventListener('click', () => addExample(2));

  document.getElementById('class-save').addEventListener('click', () => saveModel());
  document.getElementById('class-load').addEventListener('click', () => loadModel());

  while (true) {
    if (classifier.getNumClasses() > 0) {
	  // Gauti aktyvavimą iš vaizdo
      const activation = net.infer(webcamElement, 'conv_preds');
      const result = await classifier.predictClass(activation);
	  // Pasirinkti tinkamiausią klasę iš klasifikatoriaus modulio
      const classes = ['A', 'B', 'C'];
      document.getElementById('console').innerText = `
        prediction: ${classes[result.classIndex]}\n
        probability: ${result.confidences[result.classIndex]}
      `;
    }
    await tf.nextFrame();
  }
}

app();
