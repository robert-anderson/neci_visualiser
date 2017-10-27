
script_string='''
var height_fac = hist_md['height']/hist_md['max_mag'];
var offset = hist_md['bar_width']/2.0;
var t_matrix = true;

function update_hists(iiter){
	$('div.slider_container span').text('iteration '+(iiter*hist_md['iter_step']));
	for (istate=0; istate<hist_md['nstates']; istate++){
		$('svg.hist_'+istate+' line.histbar').each(function(i){
			$(this).attr('y2', hist_md['height']-height_fac*hist_data[istate][iiter]['mags'][i]);
			$(this).css('stroke', hist_data[istate][iiter]['colours'][i]);
		});
			//$('svg.hist_'+istate+' line.histbar').attr('y2', hist_data[istate][iiter]['colours'][idet]+
	}
}


$(document).ready(function(){
	// attach listener to the slider and set up attributes
	$('#slider').on('change', function(){
		update_hists($(this).val());
	});
	$('#slider').attr('max', hist_md['niters']-1);
	
	hist_md['sector_positions'].push(hist_md['ndets']);

	// make svg for hamiltonian heatmap

	if (t_matrix){
		$('div.svg_root').append(
			'<svg class="heatmap" width="'+
			hist_md['ndets']*hist_md['bar_width']+
			'" height="'+
			hist_md['ndets']*hist_md['bar_width']+
			'" style="display:block"></svg>'
		);
		for (jsector=0; jsector<hist_md['sector_positions'].length; jsector++){
			for (isector=0; isector<hist_md['sector_positions'].length; isector++){
				colour = hist_md['sector_colours'][(1+isector+jsector)%hist_md['sector_colours'].length]
				$('svg.heatmap').append(
					'<rect class="histsect" x="'+
					(isector==0 ? 0 : hist_md['sector_positions'][isector-1]*hist_md['bar_width'])+
					'" y="'+
					(jsector==0 ? 0 : hist_md['sector_positions'][jsector-1]*hist_md['bar_width'])+
					'" width="'+
					(hist_md['sector_positions'][isector]*hist_md['bar_width'])+
					'" height="'+
					(hist_md['sector_positions'][jsector]*hist_md['bar_width'])+
					'" style="fill:'+colour+';stroke-width:0" />'
				);
			}
		}
		for (idet=0; idet<hist_md['ndets']; idet++){
			for (jdet=0; jdet<hist_md['ndets']; jdet++){
				if (H[idet][jdet]!='#000000'){
					$('svg.heatmap').append(
						'<line class="histbar" x1="'+
						(offset + idet*hist_md['bar_width'])+
						'" y1="'+
						(jdet*hist_md['bar_width'])+
						'" x2="'+
						(offset + (idet)*hist_md['bar_width'])+
						'" y2="'+
						((jdet+1)*hist_md['bar_width'])+
						'" style="stroke:'+H[idet][jdet]+' ;stroke-width:'+
						hist_md['bar_width']+
						'" />'
					);
				}
			}
		}
	}


	// make svgs for histograms
	for (istate=0; istate<hist_md['nstates']; istate++){
		$('div.svg_root').append(
			'<svg class=hist_'+istate+' width="'+
			hist_md['ndets']*hist_md['bar_width']+
			'" height="'+hist_md['height']+'" style="display:block"></svg>'
		);
		
		// draw sectors first:
		for (isector=0; isector<hist_md['sector_positions'].length; isector++){
			colour = hist_md['sector_colours'][isector%hist_md['sector_colours'].length]
			$('svg.hist_'+istate).append(
				'<rect class="histsect" x="'+
				(isector==0 ? 0 : hist_md['sector_positions'][isector-1]*hist_md['bar_width'])
				+'" y="0" width="'+
				(hist_md['sector_positions'][isector]*hist_md['bar_width'])+
				'" height="'+
				(hist_md['height'])+
				'" style="fill:'+colour+';stroke-width:0" />'
			);
		}

		// then empty bars:
		for (idet=0; idet<hist_md['ndets']; idet++){
			$('svg.hist_'+istate).append(
				'<line class="histbar" x1="'+
				(offset + idet*hist_md['bar_width'])+
				'" y1="'+
				hist_md['height']+
				'" x2="'+
				(offset + idet*hist_md['bar_width'])+
				'" y2="'+
				hist_md['height']+
				'" style="stroke:black ;stroke-width:'+
				hist_md['bar_width']+
				'" />'
			);
		}
	}
	// 'refresh' the container after appending nodes
	$("div.svg_root").html($("div.svg_root").html());
	update_hists(0);
});
'''
