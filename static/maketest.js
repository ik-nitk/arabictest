<!--

var questionIndex = 0;

var questions = [];

/*
   { 
   'answer': '2',
   'question': 'What doesn\'t fit?',
options: ['Dog', 'Capybara', 'Pizza']
},
{ 
'answer': '1',
'question': 'What is 9*9',
options: ['9', '81', '99']
}
];
 */
// Detect when the submit button is clicked and check if the question
// was answered correctly
function nextHandler(e) {
   var currentQuestion = null;
   e.preventDefault();
   //http://stackoverflow.com/questions/15839169/how-to-get-value-of-selected-radio-button
   correct=0;
   for(var j=0;j<questions.length;j++){ 
      currentQuestion = questions[j % questions.length];
      var checked = $("input[name='qa"+j+"']:checked", $(quiz));
      if(checked.length === 0) {
	 html = "</h2><p>" + "Please answer the question : " + (j+1) + "</p></h2>";
	 $(missdiv).html(html);
	 $.mobile.changePage('#warning', {
              transition: 'pop',
              changeHash: true,
              role: 'dialog'
          });
         return ;
       } 
       if(currentQuestion.answer == checked.val()){
         correct++;
       }
     }    
     html = "</h2><p>" + "Your score is " + correct + " of " + questions.length + "</p></h2>";
     $(scorediv).html(html);
     $.mobile.changePage('#scorepopup', {
           transition: 'pop',
           changeHash: true,
           role: 'dialog'
      });

     return true;
}

function nextButton() {
   return "<a href='' class='quiztest' data-role='button'>Test</a>";	
}

function buildQuestions() {

   var selected = [];

   /* build 5	 multiple choice quistions */
   for(var i=0;i < 5;i++)
   {
      /*select random from qalist*/
      var x = Math.floor((Math.random() * qalist.length));;

      while( selected.indexOf( x ) != -1){
	 x = Math.floor((Math.random() * qalist.length));
      }
      selected.push(x);
      /*prepare question*/
      random = { 'question': qalist[x].q, 'answer': Math.floor((Math.random() * 4)) , 'options': [] };

      for (var j=0; j<4;j++){
	 if(j== random.answer){
	    random.options.push(qalist[x].a);
	 }else{
	    random.options.push(qalist[(x+j+1)%qalist.length].a)
	 }
      }
      questions.push(random);
   }
}

// Show a random question
function showQuestions() {
   questions = [];
   buildQuestions();
   var html = "</h2><form><div data-role='fieldcontain'>";
   var questionIndex=0; 
   for(var j=0;j<questions.length;j++){
      // Grab next question, and increment so we get a new one next time
      var random = questions[questionIndex++ % questions.length];

      html += "<fieldset data-role='controlgroup'><h2>" + random.question + "</h2><div>";

      for(var i=0; i<random.options.length; i++) {
	 html += "<input type='radio' name='qa"+j+"' id='qa_"+i+""+j+"' value='"+i+"'/><label for='qa_"+i+""+j+"'>" + random.options[i] + "</label>";
      }
      html += "</div></fieldset>"
   }
   html += "</div></form>" + nextButton();

   $(quiz).html(html).trigger('create');
   $(quiz).off("click", ".quiztest", nextHandler);
   $(quiz).on("click", ".quiztest", nextHandler); 

   currentQuestion = random;
};

/* global $,document,console,quizMaster */
$(document).ready(function() {
      /*install close handler*/
      $(document).on('click','#retest',function () {
	 $('#scorepopup').dialog('close');
	 showQuestions();
	 }); 
      $(document).on('click','#missback',function () {
	 $('#warning').dialog('close');

	 }); 
      showQuestions() ;
      });

-->
