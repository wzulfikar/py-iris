# import core command "streamer"
import lib.streamer as streamer

# commands from facerec module
import modules.facerec.commands.faceadd as faceadd
import modules.facerec.commands.facefind as facefind
import modules.facerec.commands.facedb as facedb
import modules.facerec.commands.setup_db as setup_db

# register your commands here
commands = {
    'stream': streamer,
    'faceadd': faceadd,
    'facedb': facedb,
    'facefind': facefind,
    'setupdb': setup_db,
}
