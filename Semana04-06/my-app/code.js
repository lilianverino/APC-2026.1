

var p5Inst = new p5(null, 'sketch');

window.preload = function () {
  initMobileControls(p5Inst);

  p5Inst._predefinedSpriteAnimations = {};
  p5Inst._pauseSpriteAnimationsByDefault = false;
  var animationListJSON = {"orderedKeys":["1f74db70-b622-44db-8a3a-2b55ebc00ebc","9adcc153-1acb-4f65-83f5-f8cf373d8212","e3bbe4af-bde4-4842-be67-4008fc8d97a1","ff8fa7d2-c2af-49ae-a69b-1dc58cc78f89"],"propsByKey":{"1f74db70-b622-44db-8a3a-2b55ebc00ebc":{"name":"sapo","sourceUrl":"assets/api/v1/animation-library/gamelab/ZxtLGQfNWjQ6oe0jPgKX3y_sxJxeirR3/category_animals/frog.png","frameSize":{"x":391,"y":390},"frameCount":1,"looping":true,"frameDelay":2,"version":"ZxtLGQfNWjQ6oe0jPgKX3y_sxJxeirR3","categories":["animals"],"loadedFromSource":true,"saved":true,"sourceSize":{"x":391,"y":390},"rootRelativePath":"assets/api/v1/animation-library/gamelab/ZxtLGQfNWjQ6oe0jPgKX3y_sxJxeirR3/category_animals/frog.png"},"9adcc153-1acb-4f65-83f5-f8cf373d8212":{"name":"mosca","sourceUrl":"assets/api/v1/animation-library/gamelab/oSoT3OtUjenPzKavo0ff9HsiHKUPAGol/category_animals/fly_1.png","frameSize":{"x":400,"y":400},"frameCount":1,"looping":true,"frameDelay":2,"version":"oSoT3OtUjenPzKavo0ff9HsiHKUPAGol","categories":["animals"],"loadedFromSource":true,"saved":true,"sourceSize":{"x":400,"y":400},"rootRelativePath":"assets/api/v1/animation-library/gamelab/oSoT3OtUjenPzKavo0ff9HsiHKUPAGol/category_animals/fly_1.png"},"e3bbe4af-bde4-4842-be67-4008fc8d97a1":{"name":"start","sourceUrl":"assets/api/v1/animation-library/gamelab/4yYO_IT42.v0HIIpWPdef86pPtR4_TWf/category_icons/goldui28_result.png","frameSize":{"x":396,"y":392},"frameCount":1,"looping":true,"frameDelay":2,"version":"4yYO_IT42.v0HIIpWPdef86pPtR4_TWf","categories":["icons"],"loadedFromSource":true,"saved":true,"sourceSize":{"x":396,"y":392},"rootRelativePath":"assets/api/v1/animation-library/gamelab/4yYO_IT42.v0HIIpWPdef86pPtR4_TWf/category_icons/goldui28_result.png"},"ff8fa7d2-c2af-49ae-a69b-1dc58cc78f89":{"name":"Lu","sourceUrl":"assets/api/v1/animation-library/gamelab/6ilCPXzP1HUKGzaSpg6oHUcE.Nv8KRqD/category_faces/kidportrait_08.png","frameSize":{"x":352,"y":399},"frameCount":1,"looping":true,"frameDelay":2,"version":"6ilCPXzP1HUKGzaSpg6oHUcE.Nv8KRqD","categories":["faces"],"loadedFromSource":true,"saved":true,"sourceSize":{"x":352,"y":399},"rootRelativePath":"assets/api/v1/animation-library/gamelab/6ilCPXzP1HUKGzaSpg6oHUcE.Nv8KRqD/category_faces/kidportrait_08.png"}}};
  var orderedKeys = animationListJSON.orderedKeys;
  var allAnimationsSingleFrame = false;
  orderedKeys.forEach(function (key) {
    var props = animationListJSON.propsByKey[key];
    var frameCount = allAnimationsSingleFrame ? 1 : props.frameCount;
    var image = loadImage(props.rootRelativePath, function () {
      var spriteSheet = loadSpriteSheet(
          image,
          props.frameSize.x,
          props.frameSize.y,
          frameCount
      );
      p5Inst._predefinedSpriteAnimations[props.name] = loadAnimation(spriteSheet);
      p5Inst._predefinedSpriteAnimations[props.name].looping = props.looping;
      p5Inst._predefinedSpriteAnimations[props.name].frameDelay = props.frameDelay;
    });
  });

  function wrappedExportedCode(stage) {
    if (stage === 'preload') {
      if (setup !== window.setup) {
        window.setup = setup;
      } else {
        return;
      }
    }
// -----


// Variaveis:
var score = 0;
var startGameScreen = true;
var mosca1Sapo = false;
var mosca2Sapo = false;
var mosca3Sapo = false;

//Sprites
var sapo = createSprite(80, 330);
sapo.setAnimation("sapo");
sapo.scale = 0.4;

var button = createSprite(300, 280);
button.setAnimation("start");
button.scale = 0.2;

var mosca1 = createSprite(200, 160);
mosca1.setAnimation("mosca");
mosca1.scale = 0.1;
mosca1.visible = false;

var mosca2 = createSprite(270, 50);
mosca2.setAnimation("mosca");
mosca2.scale = 0.1;
mosca2.visible = false;

var mosca3 = createSprite(300, 265);
mosca3.setAnimation("mosca");
mosca3.scale = 0.1;
mosca3.visible = false;


var player = createSprite(100, 50);
player.setAnimation("Lu");
player.scale = 0.2;
player.visible = false;



//Loop
function draw() {
  // desenhado fundo
  if(mousePressedOver(button)){
    startGameScreen = false;
  }
  //mudando o fundo quando aperta o start (aparece as moscas)
  if(startGameScreen){
    drawStartBackground();
  }else{
    drawPlayBackground();
  }
  
  //movendo a Lu com as setas
  if (keyDown("up")) {
    player.y=player.y-2;
  }
  if (keyDown("down")) {
    player.y=player.y+2;
  }
  if (keyDown("left")) {
    player.x=player.x-2;
  }
  if (keyDown("right")) {
    player.x=player.x+2;
  }
  
  //movendo as moscas quando a Lu as toca
  if(player.isTouching(mosca1)){
    player.displace(mosca1);
  }
  if(player.isTouching(mosca2)){
    player.displace(mosca2);
  }
  if(player.isTouching(mosca3)){
    player.displace(mosca3);
  }
  
  //colocando as moscas no sapo
  if(mosca1.isTouching(sapo) && mosca1Sapo == false){
    mosca1.x = 10;
    mosca1.y = 375;
    score ++;
    mosca1Sapo = true;
  }
  if(mosca2.isTouching(sapo) && mosca2Sapo == false){
    mosca2.x = 40;
    mosca2.y = 375;
    score ++;
    mosca2Sapo = true;
  }
  if(mosca3.isTouching(sapo) && mosca3Sapo == false){
    mosca3.x = 70;
    mosca3.y = 375;
    score ++;
    mosca3Sapo = true;
  }
  
  //Parabens quando o sapo pegar todas as moscas
  if(score == 3){
    textSize(50);
    textAlign(CENTER, CENTER);
    fill("yellow");
    text("Você ajudou a Lu!", 0, 0, 400, 200);
  }
  
  
  // atualizando sprites
  drawSprites();
}


//Desenhando a tela inicial e do jogo
function drawStartBackground(){
  background("deepskyblue");
  textFont("Ariel");
  textSize(20);
  textAlign(CENTER);
  text("Ajude Lu a alimentar o sapo dela. Aperte o botão pra começar!", 90, 50, 270, 400);
}
function drawPlayBackground(){
  background("deepskyblue");
  textFont("Ariel");
  textSize(20);
  textAlign(CENTER, TOP);
  text("Moscas comidas: " + score, 0, 0, 400, 200);
  fill("yellow");
  mosca1.visible = true;
  button.visible = false;
  player.visible = true;
  mosca2.visible = true;
  mosca3.visible = true;
  sapo.visible = true;
}

// -----
    try { window.draw = draw; } catch (e) {}
    switch (stage) {
      case 'preload':
        if (preload !== window.preload) { preload(); }
        break;
      case 'setup':
        if (setup !== window.setup) { setup(); }
        break;
    }
  }
  window.wrappedExportedCode = wrappedExportedCode;
  wrappedExportedCode('preload');
};

window.setup = function () {
  window.wrappedExportedCode('setup');
};
