
var OHMS = {

    no_pattern_alpha : function(){
        if ($('.pat-filter-alpha').length == 0){
            $('#ohms-results .ohms-file').each(function(){
                $(this).show();
            });
        }
    },

    pattern_alpha : function() {
    
        // var abcs = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','all'];
        var abcsset = {};
        $('.pat-filter-alpha-result').each(function(i, e){
            var abc = $(this).attr('data-abc');
            abcsset[abc] = abc;
        })
       
        var abcs = $.map(abcsset, function(el) { return el });
        abcs.sort();
        abcs.push('all');
        
    
        $('.pat-filter-alpha').each(function(){
        
            for(var i in abcs) {
                var abc = abcs[i];
                var span = $('<span>').text(abc.toUpperCase()).attr('data-abc', abc).click(function(){
                    var o = this;
                    $('#ohms-results .ohms-file').each(function(){
                        
                        $(this).hide();
                        
                        if ($(this).attr('data-abc') == $(o).attr('data-abc'))
                            $(this).fadeIn(250);
                        else if ($(o).attr('data-abc') == 'all')
                            $(this).fadeIn(250);
                    });
                    
                    
                    OHMS.pattern_shortner_hide_all();
                });
                $(this).append(span);
            }
            
        });
        
    },

    pattern_selector : function() {
        $('select.pat-filter-selector').each(function(){
        
            $(this).change(function(){
                var selected = $.trim($(this).find('option:selected').val());     
                
                $('#ohms-results .ohms-file').each(function(){
                    $(this).hide();
                    if ($(this).attr('data-subject_headings').indexOf(selected) != -1)
                        $(this).fadeIn(250);
                });
                
                OHMS.pattern_shortner_hide_all();
            });
        });
    
    },
    
    pattern_searchtext : function() {
        $('input.pat-filter-searchtext').each(function(){
            
            $(this).keyup(function(){
                var query = $(this).val().toLowerCase();
                $('#ohms-results .ohms-file').each(function(){
                    $(this).hide();
                    if ($(this).attr('data-subject_headings').toLowerCase().indexOf(query) != -1 || 
                        $(this).find('.ohms-title').text().toLowerCase().indexOf(query) != -1 || 
                        $(this).find('.ohms-desc').text().toLowerCase().indexOf(query) != -1)
                        $(this).fadeIn(250);
                });
                
            });
        });
    
    },
    
    
    pattern_shortner: function() {
        $('.pat-shortner').each(function(){
            var text = $.trim($(this).text());
            
            var first = text.substring(0, 200);
            var last = text.substring(200, text.length);
            
            var sm = $('<span>').addClass('showmore').html('Show more').click(function(){
                $(this).parent().find('.showmore-content').show();
                $(this).hide();
            });
            var smc = $('<span>').addClass('showmore-content').html(last).hide();
            
            $(this).html(first);
            $(this).append(sm);
            $(this).append(smc);
        });
    
    },
    
    pattern_shortner_hide_all: function() {
        $('.pat-shortner').each(function(){
            $('.showmore').show();
            $('.showmore-content').hide();
        });
    
    },
    
    
}



$(document).ready(function(){
    OHMS.pattern_selector();
    OHMS.pattern_alpha();
    OHMS.pattern_searchtext();
    OHMS.pattern_shortner();
    OHMS.no_pattern_alpha();
});