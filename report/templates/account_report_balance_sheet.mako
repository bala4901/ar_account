<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 	<head> 
		<meta content="text/html; charset=UTF-8" http-equiv="content-type"/> 
		<script> 
			function subst() { 
				var vars={}; 
				var x=document.location.search.substring(1).split('&'); 
				for(var i in x) {
					var z=x[i].split('=',2);
					vars[z[0]] = unescape(z[1]);} 
				var x=['frompage','topage','page','webpage','section','subsection','subsubsection']; 
				for(var i in x) { 
					var y = document.getElementsByClassName(x[i]); 
					for(var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]]; } } 
		</script> 
		<style type="text/css"> 
			${css} 
		</style> 
	</head>
	<body style="border:0; margin: 0;" onload="subst()"> 
        <div class="act_as_table data_table">
            <div class="act_as_row labels">
		            <div class="act_as_cell">${_('Aktiva')}</div>
		            <div class="act_as_cell"> </div>
		            <div class="act_as_cell"> </div>

		            <div class="act_as_cell"> </div>
		            <div class="act_as_cell"> </div>
		            <div class="act_as_cell">${_('Pasiva')}</div>
			</div>
            <div class="act_as_row labels">
		            <div class="act_as_cell">${_('Account')}</div>
		            <div class="act_as_cell">${_('Year To Date')}</div>
		            <div class="act_as_cell">${_('Balance')}</div>

		            <div class="act_as_cell">${_('Account')}</div>
		            <div class="act_as_cell">${_('Year To Date')}</div>
		            <div class="act_as_cell">${_('Balance')}</div>
			</div>
			%for account in objects:
			    <div class="act_as_row">
			        <div class="act_as_cell">${objects}</div>
				</div>
			%endfor
		</div>

    </body>
</html>

