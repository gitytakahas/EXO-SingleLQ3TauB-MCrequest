for mass in 200 400 600 700 800 900 1000 1200 1500 2000 
do
#    cp -r ../s-${mass}/Cards/proc_card_mg5.dat s-${mass}/
#    cp -r ../t-${mass}/Cards/proc_card_mg5.dat t-${mass}/
    sed -i -e "s/output s-template/output s-"${mass}"/" s-${mass}/proc_card_mg5.dat
    sed -i -e "s/output t-template/output t-"${mass}"/" t-${mass}/proc_card_mg5.dat
#    cp -r 
done