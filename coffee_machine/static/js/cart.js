// <!DOCTYPE html>
// {% load static %}
// <html>
// <head>
// 	<title>Ecom</title>
//
// 	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1" />
//
// 	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
//
// 	<link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}">
//
// </head>
// <body>
//
// 	<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
// 	  <a class="navbar-brand" href="{% url 'store' %}">Ecom</a>
// 	  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
// 	    <span class="navbar-toggler-icon"></span>
// 	  </button>
//
// 	  <div class="collapse navbar-collapse" id="navbarSupportedContent">
// 	    <ul class="navbar-nav mr-auto">
// 	      <li class="nav-item active">
// 	        <a class="nav-link" href="{% url 'store' %}">Store <span class="sr-only">(current)</span></a>
// 	      </li>
//
// 	    </ul>
// 	    <div class="form-inline my-2 my-lg-0">
// 	     	<a href="#"class="btn btn-warning">Login</a>
//
// 	     	<a href="{% url 'cart' %}">
// 	    		<img  id="cart-icon" src="{% static 'images/cart.png' %}">
// 	    	</a>
// 	    	<p id="cart-total">0</p>
//
// 	    </div>
// 	  </div>
// 	</nav>
//
//      <div class="container">
//             <br>
//             {% block content %}
//
//
//             {% endblock content %}
//          </div>
//
//
// 	<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
//
// 	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
//
// 	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
//
// 	<script type="text/javascript" src="{% static 'js/cart.js' %}"></script>
// </body>
// </html>