(this.webpackJsonprecipes=this.webpackJsonprecipes||[]).push([[0],{112:function(e,t,n){e.exports=n(232)},117:function(e,t,n){},118:function(e,t,n){},232:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),c=n(15),o=n.n(c),i=(n(117),n(27)),l=n(28),s=n(29),u=n(30),p=(n(118),n(240)),h=n(241),m=n(239),d=n(242),f=function(e){Object(u.a)(n,e);var t=Object(s.a)(n);function n(){return Object(i.a)(this,n),t.apply(this,arguments)}return Object(l.a)(n,[{key:"render",value:function(){return r.a.createElement(p.a.Item,null,r.a.createElement(p.a.Content,null,r.a.createElement(p.a.Header,null,this.props.ingredient.name),r.a.createElement(p.a.Description,null,this.props.ingredient.spoken)))}}]),n}(r.a.Component),v=function(e){Object(u.a)(n,e);var t=Object(s.a)(n);function n(){return Object(i.a)(this,n),t.apply(this,arguments)}return Object(l.a)(n,[{key:"render",value:function(){var e=[];return console.log(this.props.ingredients),this.props.ingredients.forEach((function(t){e.push(r.a.createElement(f,{ingredient:t}))})),r.a.createElement(p.a,{horizontal:!1},e)}}]),n}(r.a.Component),E=function(e){Object(u.a)(n,e);var t=Object(s.a)(n);function n(){return Object(i.a)(this,n),t.apply(this,arguments)}return Object(l.a)(n,[{key:"render",value:function(){var e=[];return this.props.instructions.forEach((function(t){e.push(r.a.createElement(p.a.Item,null,t))})),r.a.createElement(p.a,null,e)}}]),n}(r.a.Component),b=function(e){Object(u.a)(n,e);var t=Object(s.a)(n);function n(e){var a;return Object(i.a)(this,n),(a=t.call(this,e)).state={error:null,isLoaded:!1,recipe:null},a}return Object(l.a)(n,[{key:"componentDidMount",value:function(){var e=this,t="https://recipes.oram.ca";"localhost"===window.location.hostname&&(t="http://localhost:5000"),fetch("".concat(t,"/api/v0/recipe/recipe_da2ddeea30c98822dbfa6182dc4f465a100e919d438691913bc8a1c7")).then((function(e){return e.json()})).then((function(t){e.setState({isLoaded:!0,recipe:t})}))}},{key:"render",value:function(){var e=[],t=[];return null!==this.state.recipe&&(e=this.state.recipe.ingredients,t=this.state.recipe.instructions),console.log(this.state.recipe),r.a.createElement("div",{className:"App"},r.a.createElement(h.a,{centered:!0,columns:2},r.a.createElement(h.a.Column,null,r.a.createElement(m.a,{position:"left"},r.a.createElement(d.a,null,r.a.createElement(v,{ingredients:e}))),r.a.createElement(d.a,null,r.a.createElement(E,{instructions:t})))))}}]),n}(r.a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));n(231);o.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(b,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[112,1,2]]]);
//# sourceMappingURL=main.dcc4dd59.chunk.js.map