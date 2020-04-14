*CREATING, EDITING, and IMPLEMENTING A SCHEME FOR LEO 
*DRAFT 1

clear
ssc install grstyle, replace
ssc install palettes, replace

*help grstyle // if necessary 
*===========================================*
* A) BREAKING DOWN A SCHEME: 
*===========================================*
* RESOURCES 
*===========================================*
** Using GRSTYLE to create new schemes:  
**http://repec.sowi.unibe.ch/stata/grstyle/getting-started.html#intro
** Graph Style features 
**http://repec.sowi.unibe.ch/stata/grstyle/help-grstyle-set.html
** Grsyle Set Color 
**http://repec.sowi.unibe.ch/stata/grstyle/help-grstyle-set.html#color
** Color Palette 
**http://repec.sowi.unibe.ch/stata/palettes/help-colorpalette.html
** Colorlist
**http://repec.sowi.unibe.ch/stata/palettes/help-colorpalette.html#colorlist
** Specifying Colors 
**http://repec.sowi.unibe.ch/stata/grstyle/help-grstyle-set.html#colorspec
*===========================================*


*===========================================*
*Set initial color scheme that will be copied and overwritten
*===========================================*

set scheme s1color

*===========================================*
*Write new color palette, in this case, using varying 
*opacities of LEO Purple, Gold, and Gray 
*===========================================*

cap program drop colorpalette_LEO
program colorpalette_LEO
            c_local P 68 43 122,208 161 0,128 128 128,68 43 122*.7,208 161 0*.7,169 169 169, ///
					  68 43 122*.4,208 161 0*.4,192 192 192,68 43 122*.2,208 161 0*.2,211 211 211 ///
                      
			
            c_local I default,primary,gray1, default.7, primary.7, gray.7, ///
					  default.4, primary.4, gray.4, default.2, primary.2, gray.2 ///
                  
        end
colorpalette LEO, rows(5)

*===========================================*
*if you not running Stata15, run this blocked out code instead of above code
*===========================================*
/* program colorpalette_LEOm
            c_local P 68 43 122,208 161 068,128 128 128,68 43 122%.7,208 161 0%.7,169 169 169, ///
					  68 43 122%.4,208 161 0%.4,192 192 192,68 43 122%.2,208 161 0%.2,211 211 211 ///
                     
			
            c_local I default,primary,gray1,secondary, default.7, primary.7, gray.7, secondary.7, ///
					  default.4, primary.4, gray.4, secondary.4, default.2, primary.2, gray.2, secondary.2 ///
                  
        end	*/
*===========================================*

*Displays Palette 
colorpalette LEO, rows(5) 
 
 *===========================================*
 *Custom Line Palette (This can be used depending on needs)
 *http://repec.sowi.unibe.ch/stata/grstyle/help-grstyle-set.html#color
 *===========================================*
 
 cap program drop linepalette_LEOsolid
 program linepalette_LEOsolid
            c_local P 1,1,1,1,1,1
            c_local I solid1,solid2,solid3, solid4, solid5, solid6
        end
linepalette LEOsolid

*===========================================* 
*initialize your scheme, with specified name:
*===========================================*
 
 if strpos("`c(machine_type)'","Mac")>0 {
	global schpath "~/Library/Application Support/Stata/ado/plus/"
}
else {
	global schpath "C:\ado"
}
 
 grstyle init LEO, replace path(${schpath})  // initializes new scheme 
 
*===========================================*
*B) PERFORMING CHANGES ON A SCHEME (specified for LEO, but all options 
*in help files and links above). 
*===========================================*

*COLOR SCHEME*
	grstyle set color LEO
	grstyle set color LEO : histogram
	grstyle set color LEO : histogram_line
    grstyle set color LEO : sunflowerlb sunflower  // light sunflower background color
    grstyle set color LEO : sunflowerdb   // dark sunflower background color
    grstyle set color lean : sunflowerlf   // light sunflower line color
    grstyle set color LEO : sunflowerdf   // dark sunflower line color

*FIX SIZE (x,y) OF GRAPH*
	*grstyle graphsize x 4
	*grstyle graphsize y 4 // create compact graph of a specified dimensions each time 
*LEGEND PLACEMENT (STANDARDIZE)
	*grstyle set legend 3, nobox // sets legend placement with no box
*BACKGROUND STYLE*		
	grstyle set plain, nogrid  // white, no grid, no boxed axes
*CONFIDENCE INTERVAL STYLE* 
	grstyle set ci LEO, select(2 1) // selects colors, can select opacity  
*FONT/TYPEFACE SET*
	graph set window fontface "Garamond" // ND Academic Font 
	*graph set window fontface "Galaxie Polaris Light" // ND licensed "modern font" 
	*graph set window fontface "Ariel " // alternative font for those who do not have Galaxie Polaris installed on their machine 
*LINE WIDTH, TITLES, & HEADERS*
	grstyle linewidth plineplot medthick
	grstyle set size 12pt: heading
	grstyle set size 8pt: subheading axis_title
	grstyle set linewidth .5pt: axisline tick major_grid legend 
	grstyle set linewidth  2pt: xyline  
*LINE PATTERNS*	
    grstyle set lpattern default: p#line // sets the palette lpattern for connected line plots
    grstyle set lpattern LEOsolid: p#lineplot // sets the palette lpattern
	grstyle set lpattern solid: ci_area 

	

*MARKERS*
	symbolpalette default  //options to customize exist, but default is sufficient right now 


	

*===========================================*
*C) SAMPLE GRAPHS WITH THIS SCHEME:
*===========================================*

**SCATTER 
	sysuse auto, clear	
	separate price, by(rep) shortlabel
	scatter price? weight
**TWO WAY W/CI
	two (scatter price length) (lpolyci price length if foreign==0) (lpolyci price length if foreign==1, astyle(ci2)), legend(off)
**BAR GRAPH
	sysuse nlsw88, clear
	graph bar wage if occ<9, over(occ) asyvars over(union)
**BAR GRAPH
	sysuse nlsw88, clear
	hist wage, scheme(LEO)
*ANOTHER TWO-WAY
	sysuse auto, clear
	two (scatter price length if foreign) (scatter price length if !foreign) 
*LINE SOLID*
    sysuse uslifeexp, clear
    line le_wfemale le_wmale le_bfemale le_bmale year, title("Title (10pt)") subtitle("Subtitle (8pt)")
*LINE VARIABLE*
    sysuse uslifeexp, clear
	grstyle set lpattern default: p#lineplot // sets the palette lpattern
    line le_wfemale le_wmale le_bfemale le_bmale year, title("Title (10pt)") subtitle("Subtitle (8pt)")
*TWOWAY*	
	sysuse auto, clear
    two (scatter price weight) (lpoly price weight), xline(4000)
*SUNFLOWER PLOT*
	webuse auto
	sunflower mpg displ	
*PIE PLOT*
	sysuse auto, clear
	graph pie  length mpg turn headroom 
*XTLINE PLOT*
	use http://www.stata-press.com/data/r13/xtline1
	xtset person day
	xtline calories, tlabel(#3)
	xtline calories, overlay

*===========================================*
*D) SAVING YOUR SCHEME, VIEWING CURRENT SETTINGS,
* & ERASING SCHEMES 
*===========================================*

*===========================================*
*VIEW CURRENT SETTINGS  
grstyle type // get all grstyle settings currently in myscheme
*VIEW WHERE THE SCHEME IS STORED LOCALLY
capture noisily findfile scheme-LEO.scheme
*DELETE SCHEME 
//grstyle LEO clear , erase 
*===========================================*	
	
*===========================================*	
*E)TO IMPLEMENT A SCHEME 
*===========================================*
*simply type "scheme(LEO)" as an option when graphing
*
*EX. 
	sysuse auto, clear
	scatter price headroom, title("Headroom v. Price") subtitle("Scheme test") scheme(LEO)
	
*End of File 
